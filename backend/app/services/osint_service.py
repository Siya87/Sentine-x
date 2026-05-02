"""
OSINT Investigation Service
Orchestrates OSINT data collection and analysis
"""
from app.models.osint import (
    OSINTInvestigationRequest,
    OSINTInvestigationResponse,
    InvestigationType,
    RiskLevel,
    DataSource,
    BreachInfo,
    SocialProfile,
    DomainInfo,
    IPInfo
)
from app.integrations.haveibeenpwned import HaveIBeenPwnedClient
from app.integrations.abuseipdb import AbuseIPDBClient
from app.integrations.virustotal import VirusTotalClient
from app.services.ai_service import AIService
from app.database.mongodb import get_database
import logging
import uuid
from datetime import datetime
import time
from typing import List, Dict, Optional, cast, Any

logger = logging.getLogger(__name__)


class OSINTService:
    """Service for OSINT investigations"""
    
    def __init__(self):
        self.hibp_client = HaveIBeenPwnedClient()
        self.abuseipdb_client = AbuseIPDBClient()
        self.virustotal_client = VirusTotalClient()
        self.ai_service = AIService()
    
    async def investigate(self, request: OSINTInvestigationRequest) -> OSINTInvestigationResponse:
        """
        Perform OSINT investigation
        
        Args:
            request: Investigation request
            
        Returns:
            Investigation results
        """
        start_time = time.time()
        investigation_id = f"osint-{uuid.uuid4()}"
        
        logger.info(f"Starting OSINT investigation: {investigation_id} for {request.target}")
        
        # Collect data based on investigation type
        data_sources = []
        breaches = []
        social_profiles = []
        domain_info = None
        ip_info = None
        
        if request.investigation_type == InvestigationType.EMAIL:
            data_sources, breaches, social_profiles = await self._investigate_email(
                request.target,
                request.include_breaches,
                request.include_social
            )
        
        elif request.investigation_type == InvestigationType.USERNAME:
            data_sources, social_profiles = await self._investigate_username(
                request.target,
                request.include_social
            )
        
        elif request.investigation_type == InvestigationType.DOMAIN:
            data_sources, domain_info = await self._investigate_domain(request.target)
        
        elif request.investigation_type == InvestigationType.IP_ADDRESS:
            data_sources, ip_info = await self._investigate_ip(request.target)
        
        elif request.investigation_type == InvestigationType.PHONE:
            data_sources = await self._investigate_phone(request.target)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(
            breaches=breaches,
            ip_info=ip_info,
            data_sources=data_sources
        )
        
        risk_level = self._determine_risk_level(risk_score)
        
        # Generate AI summary and recommendations
        summary, findings, recommendations = await self._generate_ai_analysis(
            investigation_type=request.investigation_type,
            target=request.target,
            breaches=breaches,
            social_profiles=social_profiles,
            domain_info=domain_info,
            ip_info=ip_info,
            risk_score=risk_score
        )
        
        # Calculate statistics
        sources_checked = len(data_sources)
        sources_found = sum(1 for ds in data_sources if ds.found)
        
        scan_duration = time.time() - start_time
        
        # Create response
        response = OSINTInvestigationResponse(
            investigation_id=investigation_id,
            investigation_type=request.investigation_type,
            target=request.target,
            risk_level=risk_level,
            risk_score=risk_score,
            data_sources=data_sources,
            breaches=breaches,
            social_profiles=social_profiles,
            domain_info=domain_info,
            ip_info=ip_info,
            summary=summary,
            findings=findings,
            recommendations=recommendations,
            sources_checked=sources_checked,
            sources_found=sources_found,
            created_at=datetime.utcnow(),
            scan_duration=round(scan_duration, 2)
        )
        
        # Store in database
        await self._store_investigation(response)
        
        logger.info(f"OSINT investigation completed: {investigation_id}")
        
        return response
    
    async def _investigate_email(
        self,
        email: str,
        include_breaches: bool,
        include_social: bool
    ) -> tuple:
        """Investigate an email address"""
        data_sources = []
        breaches = []
        social_profiles = []
        
        # Check HaveIBeenPwned
        if include_breaches:
            breach_data = await self.hibp_client.check_email(email)
            if breach_data:
                data_sources.append(DataSource(
                    name="HaveIBeenPwned",
                    url="https://haveibeenpwned.com",
                    found=len(breach_data) > 0,
                    data={"breach_count": len(breach_data)}
                ))
                
                # Convert to BreachInfo objects
                for breach in breach_data[:10]:  # Limit to 10 most recent
                    breaches.append(BreachInfo(
                        breach_name=breach.get("Name", "Unknown"),
                        breach_date=breach.get("BreachDate"),
                        compromised_data=breach.get("DataClasses", []),
                        description=breach.get("Description", ""),
                        verified=breach.get("IsVerified", False)
                    ))
        
        # Mock social media search (would integrate with real APIs)
        if include_social:
            social_profiles = self._mock_social_profiles(email)
            if social_profiles:
                data_sources.append(DataSource(
                    name="Social Media Search",
                    found=True,
                    data={"profiles_found": len(social_profiles)}
                ))
        
        return data_sources, breaches, social_profiles
    
    async def _investigate_username(self, username: str, include_social: bool) -> tuple:
        """Investigate a username"""
        data_sources = []
        social_profiles = []
        
        if include_social:
            social_profiles = self._mock_social_profiles(username)
            if social_profiles:
                data_sources.append(DataSource(
                    name="Username Search",
                    found=True,
                    data={"profiles_found": len(social_profiles)}
                ))
        
        return data_sources, social_profiles
    
    async def _investigate_domain(self, domain: str) -> tuple:
        """Investigate a domain"""
        data_sources = []
        
        # Check VirusTotal
        vt_data = await self.virustotal_client.get_domain_info(domain)
        if vt_data:
            data_sources.append(DataSource(
                name="VirusTotal",
                url="https://www.virustotal.com",
                found=True,
                data=vt_data
            ))
        
        # Mock domain info (would use WHOIS API)
        domain_info = DomainInfo(
            domain=domain,
            registrar="Example Registrar",
            creation_date="2020-01-15",
            expiration_date="2027-01-15",
            name_servers=["ns1.example.com", "ns2.example.com"],
            status="active"
        )
        
        data_sources.append(DataSource(
            name="WHOIS Lookup",
            found=True,
            data={"registrar": domain_info.registrar}
        ))
        
        return data_sources, domain_info
    
    async def _investigate_ip(self, ip_address: str) -> tuple:
        """Investigate an IP address"""
        data_sources = []
        
        # Check AbuseIPDB
        abuse_data = await self.abuseipdb_client.check_ip(ip_address)
        if abuse_data:
            data_sources.append(DataSource(
                name="AbuseIPDB",
                url="https://www.abuseipdb.com",
                found=True,
                data={
                    "abuse_score": abuse_data.get("abuse_confidence_score", 0),
                    "total_reports": abuse_data.get("total_reports", 0)
                }
            ))
            
            ip_info = IPInfo(
                ip=ip_address,
                country=abuse_data.get("country_name"),
                city=None,  # Would need GeoIP database
                isp=abuse_data.get("isp"),
                abuse_score=abuse_data.get("abuse_confidence_score", 0),
                is_vpn=abuse_data.get("usage_type") == "VPN",
                is_proxy=abuse_data.get("usage_type") == "Proxy"
            )
        else:
            ip_info = None
        
        return data_sources, ip_info
    
    async def _investigate_phone(self, phone: str) -> List[DataSource]:
        """Investigate a phone number"""
        # Mock phone investigation (would integrate with phone lookup APIs)
        return [
            DataSource(
                name="Phone Lookup",
                found=True,
                data={"carrier": "Example Carrier", "type": "mobile"}
            )
        ]
    
    def _calculate_risk_score(
        self,
        breaches: List[BreachInfo],
        ip_info: Optional[IPInfo],
        data_sources: List[DataSource]
    ) -> int:
        """Calculate overall risk score (0-100)"""
        score = 0
        
        # Breach score (up to 40 points)
        if breaches:
            breach_score = min(len(breaches) * 10, 40)
            score += breach_score
        
        # IP abuse score (up to 40 points)
        if ip_info and ip_info.abuse_score:
            score += min(ip_info.abuse_score * 0.4, 40)
        
        # Data exposure score (up to 20 points)
        exposure_score = min(len([ds for ds in data_sources if ds.found]) * 5, 20)
        score += exposure_score
        
        return min(int(score), 100)
    
    def _determine_risk_level(self, risk_score: int) -> RiskLevel:
        """Determine risk level from score"""
        if risk_score >= 75:
            return RiskLevel.CRITICAL
        elif risk_score >= 50:
            return RiskLevel.HIGH
        elif risk_score >= 25:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    async def _generate_ai_analysis(
        self,
        investigation_type: InvestigationType,
        target: str,
        breaches: List[BreachInfo],
        social_profiles: List[SocialProfile],
        domain_info: Optional[DomainInfo],
        ip_info: Optional[IPInfo],
        risk_score: int
    ) -> tuple:
        """Generate AI-powered analysis"""
        
        # Create context for AI
        context = f"OSINT Investigation for {investigation_type.value}: {target}\n"
        context += f"Risk Score: {risk_score}/100\n\n"
        
        if breaches:
            context += f"Data Breaches Found: {len(breaches)}\n"
            for breach in breaches[:3]:
                context += f"- {breach.breach_name} ({breach.breach_date})\n"
        
        if social_profiles:
            context += f"\nSocial Profiles: {len(social_profiles)}\n"
        
        if ip_info:
            context += f"\nIP Abuse Score: {ip_info.abuse_score}\n"
            context += f"ISP: {ip_info.isp}\n"
        
        # Generate AI summary
        summary_data = {
            "target": target,
            "target_type": investigation_type.value,
            "breach_data": [b.model_dump() for b in breaches] if breaches else [],
            "ip_reputation": ip_info.model_dump() if ip_info else {},
            "social_profiles": [p.model_dump() for p in social_profiles] if social_profiles else []
        }
        ai_summary = await self.ai_service.generate_osint_summary(summary_data)
        
        # Extract summary text from AI response
        summary = ai_summary.get("summary", "Investigation completed")
        
        # Generate findings (use AI findings if available, otherwise generate)
        findings = ai_summary.get("key_findings", [])
        if not findings:
            if breaches:
                findings.append(f"Found in {len(breaches)} data breach(es)")
            if social_profiles:
                findings.append(f"Active on {len(social_profiles)} social platform(s)")
            if ip_info and ip_info.abuse_score and ip_info.abuse_score > 50:
                findings.append(f"High abuse confidence score: {ip_info.abuse_score}%")
        
        # Generate recommendations (use AI recommendations if available, otherwise generate)
        recommendations = ai_summary.get("recommendations", [])
        if not recommendations:
            if breaches:
                recommendations.append("Change passwords for all affected accounts")
                recommendations.append("Enable two-factor authentication")
            if risk_score > 50:
                recommendations.append("Monitor for suspicious activity")
                recommendations.append("Consider additional security measures")
        
        return summary, findings, recommendations
    
    def _mock_social_profiles(self, identifier: str) -> List[SocialProfile]:
        """Generate mock social profiles"""
        return [
            SocialProfile(
                platform="Twitter",
                username=identifier.split('@')[0] if '@' in identifier else identifier,
                url=f"https://twitter.com/{identifier}",
                followers=1250,
                verified=False
            ),
            SocialProfile(
                platform="LinkedIn",
                username=identifier.split('@')[0] if '@' in identifier else identifier,
                url=f"https://linkedin.com/in/{identifier}",
                verified=False
            )
        ]
    
    async def _store_investigation(self, investigation: OSINTInvestigationResponse):
        """Store investigation in database"""
        try:
            db = cast(Any, get_database())
            
            await db.osint_investigations.insert_one(investigation.model_dump(mode='json'))
            logger.info(f"Stored investigation: {investigation.investigation_id}")
        except Exception as e:
            logger.error(f"Failed to store investigation: {e}")
    
    async def get_investigation(self, investigation_id: str) -> Optional[OSINTInvestigationResponse]:
        """Get investigation by ID"""
        try:
            db = cast(Any, get_database())
            
            doc = await db.osint_investigations.find_one({"investigation_id": investigation_id})
            if doc:
                doc.pop('_id', None)
                return OSINTInvestigationResponse(**doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get investigation: {e}")
            return None
    
    async def get_investigation_history(self, limit: int = 10, skip: int = 0) -> List[OSINTInvestigationResponse]:
        """Get investigation history"""
        try:
            db = cast(Any, get_database())
            
            cursor = db.osint_investigations.find().sort("created_at", -1).skip(skip).limit(limit)
            investigations = []
            
            async for doc in cursor:
                doc.pop('_id', None)
                investigations.append(OSINTInvestigationResponse(**doc))
            
            return investigations
        except Exception as e:
            logger.error(f"Failed to get investigation history: {e}")
            return []
    
    async def get_statistics(self) -> Dict:
        """Get OSINT statistics"""
        try:
            db = cast(Any, get_database())
            
            total = await db.osint_investigations.count_documents({})
            
            # Aggregate by type
            by_type_pipeline = [
                {"$group": {"_id": "$investigation_type", "count": {"$sum": 1}}}
            ]
            by_type = {doc["_id"]: doc["count"] async for doc in db.osint_investigations.aggregate(by_type_pipeline)}
            
            # Aggregate by risk level
            by_risk_pipeline = [
                {"$group": {"_id": "$risk_level", "count": {"$sum": 1}}}
            ]
            by_risk = {doc["_id"]: doc["count"] async for doc in db.osint_investigations.aggregate(by_risk_pipeline)}
            
            # Average risk score
            avg_pipeline = [
                {"$group": {"_id": None, "avg_score": {"$avg": "$risk_score"}}}
            ]
            avg_result = await db.osint_investigations.aggregate(avg_pipeline).to_list(1)
            avg_risk_score = avg_result[0]["avg_score"] if avg_result else 0
            
            # Count breaches and profiles
            breach_pipeline = [
                {"$group": {"_id": None, "total": {"$sum": {"$size": "$breaches"}}}}
            ]
            breach_result = await db.osint_investigations.aggregate(breach_pipeline).to_list(1)
            total_breaches = breach_result[0]["total"] if breach_result else 0
            
            profile_pipeline = [
                {"$group": {"_id": None, "total": {"$sum": {"$size": "$social_profiles"}}}}
            ]
            profile_result = await db.osint_investigations.aggregate(profile_pipeline).to_list(1)
            total_profiles = profile_result[0]["total"] if profile_result else 0
            
            return {
                "total_investigations": total,
                "by_type": by_type,
                "by_risk_level": by_risk,
                "avg_risk_score": round(avg_risk_score, 2),
                "total_breaches_found": total_breaches,
                "total_social_profiles_found": total_profiles
            }
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {
                "total_investigations": 0,
                "by_type": {},
                "by_risk_level": {},
                "avg_risk_score": 0,
                "total_breaches_found": 0,
                "total_social_profiles_found": 0
            }

# Made with Bob
