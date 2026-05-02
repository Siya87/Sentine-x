"""
Threat Intelligence Service
Aggregates threat data from multiple sources including Shodan
"""
from app.models.threat import (
    ThreatIntelligence,
    ThreatType,
    ThreatSeverity,
    ThreatStatus,
    ThreatIndicator,
    GeoLocation,
    ThreatStatistics,
    ShodanHostInfo
)
from app.integrations.shodan import ShodanClient
from app.integrations.abuseipdb import AbuseIPDBClient
from app.database.mongodb import get_database
import logging
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, cast

logger = logging.getLogger(__name__)


class ThreatService:
    """Service for threat intelligence aggregation and analysis"""
    
    def __init__(self):
        """Initialize threat service"""
        self.shodan_client = ShodanClient()
        self.abuseipdb_client = AbuseIPDBClient()
    
    async def get_live_threats(self, limit: int = 100) -> List[ThreatIntelligence]:
        """
        Get live threat intelligence from multiple sources
        
        Args:
            limit: Maximum number of threats to return
            
        Returns:
            List of threat intelligence entries
        """
        threats = []
        
        try:
            # Get malware C2 servers from Shodan
            c2_servers = await self.shodan_client.get_malware_c2()
            for host in c2_servers[:limit//3]:
                threat = self._convert_shodan_to_threat(host, ThreatType.MALWARE)
                threats.append(threat)
            
            # Get ransomware infrastructure
            ransomware_hosts = await self.shodan_client.get_ransomware_infrastructure()
            for host in ransomware_hosts[:limit//3]:
                threat = self._convert_shodan_to_threat(host, ThreatType.RANSOMWARE)
                threats.append(threat)
            
            # Get vulnerable hosts
            vuln_hosts = await self.shodan_client.get_vulnerabilities()
            for host in vuln_hosts[:limit//3]:
                threat = self._convert_shodan_to_threat(host, ThreatType.VULNERABILITY)
                threats.append(threat)
            
            # Store threats in database
            for threat in threats:
                await self._store_threat(threat)
            
            logger.info(f"Retrieved {len(threats)} live threats")
            return threats[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get live threats: {e}")
            return []
    
    async def search_threats(
        self,
        query: Optional[str] = None,
        threat_type: Optional[ThreatType] = None,
        severity: Optional[ThreatSeverity] = None,
        status: Optional[ThreatStatus] = None,
        country: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 50,
        skip: int = 0
    ) -> tuple[List[ThreatIntelligence], int]:
        """
        Search threats in database with filters
        
        Returns:
            Tuple of (threats list, total count)
        """
        try:
            db = cast(Any, get_database())
            
            # Build query
            filters = {}
            if query:
                filters["$or"] = [
                    {"title": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}}
                ]
            if threat_type:
                filters["threat_type"] = threat_type.value
            if severity:
                filters["severity"] = severity.value
            if status:
                filters["status"] = status.value
            if country:
                filters["geo_location.country_code"] = country
            if start_date:
                filters["created_at"] = {"$gte": start_date}
            if end_date:
                if "created_at" in filters:
                    filters["created_at"]["$lte"] = end_date
                else:
                    filters["created_at"] = {"$lte": end_date}
            
            # Get total count
            total = await db.threat_intelligence.count_documents(filters)
            
            # Get threats
            cursor = db.threat_intelligence.find(filters).sort("created_at", -1).skip(skip).limit(limit)
            threats = []
            
            async for doc in cursor:
                doc.pop('_id', None)
                threats.append(ThreatIntelligence(**doc))
            
            return threats, total
            
        except Exception as e:
            logger.error(f"Failed to search threats: {e}")
            return [], 0
    
    async def get_threat_by_id(self, threat_id: str) -> Optional[ThreatIntelligence]:
        """Get specific threat by ID"""
        try:
            db = cast(Any, get_database())
            doc = await db.threat_intelligence.find_one({"threat_id": threat_id})
            
            if doc:
                doc.pop('_id', None)
                return ThreatIntelligence(**doc)
            return None
            
        except Exception as e:
            logger.error(f"Failed to get threat: {e}")
            return None
    
    async def get_statistics(self) -> ThreatStatistics:
        """Get threat statistics"""
        try:
            db = cast(Any, get_database())
            
            # Total threats
            total = await db.threat_intelligence.count_documents({})
            
            # Active threats
            active = await db.threat_intelligence.count_documents({"status": "active"})
            
            # By severity
            critical = await db.threat_intelligence.count_documents({"severity": "critical"})
            high = await db.threat_intelligence.count_documents({"severity": "high"})
            medium = await db.threat_intelligence.count_documents({"severity": "medium"})
            low = await db.threat_intelligence.count_documents({"severity": "low"})
            
            # By type
            by_type_pipeline = [
                {"$group": {"_id": "$threat_type", "count": {"$sum": 1}}}
            ]
            by_type_result = await db.threat_intelligence.aggregate(by_type_pipeline).to_list(20)
            by_type = {doc["_id"]: doc["count"] for doc in by_type_result}
            
            # By country
            by_country_pipeline = [
                {"$match": {"geo_location.country_code": {"$exists": True}}},
                {"$group": {"_id": "$geo_location.country_code", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 10}
            ]
            by_country_result = await db.threat_intelligence.aggregate(by_country_pipeline).to_list(10)
            by_country = {doc["_id"]: doc["count"] for doc in by_country_result}
            
            # Recent threats
            recent_cursor = db.threat_intelligence.find().sort("created_at", -1).limit(10)
            recent_threats = []
            async for doc in recent_cursor:
                doc.pop('_id', None)
                recent_threats.append(ThreatIntelligence(**doc))
            
            # Trending indicators
            indicator_pipeline = [
                {"$unwind": "$indicators"},
                {"$group": {
                    "_id": "$indicators.value",
                    "count": {"$sum": 1},
                    "type": {"$first": "$indicators.type"},
                    "confidence": {"$avg": "$indicators.confidence"}
                }},
                {"$sort": {"count": -1}},
                {"$limit": 10}
            ]
            indicator_result = await db.threat_intelligence.aggregate(indicator_pipeline).to_list(10)
            trending_indicators = [
                ThreatIndicator(
                    type=doc["type"],
                    value=doc["_id"],
                    confidence=int(doc["confidence"]),
                    first_seen=datetime.utcnow(),
                    last_seen=datetime.utcnow()
                )
                for doc in indicator_result
            ]
            
            return ThreatStatistics(
                total_threats=total,
                active_threats=active,
                critical_threats=critical,
                high_threats=high,
                medium_threats=medium,
                low_threats=low,
                by_type=by_type,
                by_country=by_country,
                recent_threats=recent_threats,
                trending_indicators=trending_indicators
            )
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return ThreatStatistics()
    
    async def get_host_info(self, ip: str) -> Optional[ShodanHostInfo]:
        """Get detailed host information from Shodan"""
        try:
            host_data = await self.shodan_client.get_host_info(ip)
            if not host_data:
                return None
            
            return ShodanHostInfo(
                ip=host_data.get("ip_str", ip),
                hostnames=host_data.get("hostnames", []),
                domains=host_data.get("domains", []),
                ports=host_data.get("ports", []),
                vulns=list(host_data.get("vulns", {}).keys()) if isinstance(host_data.get("vulns"), dict) else host_data.get("vulns", []),
                os=host_data.get("os"),
                organization=host_data.get("org"),
                isp=host_data.get("isp"),
                asn=host_data.get("asn"),
                country_code=host_data.get("country_code"),
                city=host_data.get("city"),
                latitude=host_data.get("latitude"),
                longitude=host_data.get("longitude"),
                last_update=datetime.fromisoformat(host_data["last_update"].replace("Z", "+00:00")) if host_data.get("last_update") else None
            )
            
        except Exception as e:
            logger.error(f"Failed to get host info: {e}")
            return None
    
    async def get_country_threats(self, country_code: str, limit: int = 50) -> List[ThreatIntelligence]:
        """Get threats from a specific country"""
        try:
            hosts = await self.shodan_client.get_country_threats(country_code)
            threats = []
            
            for host in hosts[:limit]:
                threat = self._convert_shodan_to_threat(host, ThreatType.SUSPICIOUS_IP)
                threats.append(threat)
                await self._store_threat(threat)
            
            return threats
            
        except Exception as e:
            logger.error(f"Failed to get country threats: {e}")
            return []
    
    def _convert_shodan_to_threat(self, host: Dict[str, Any], threat_type: ThreatType) -> ThreatIntelligence:
        """Convert Shodan host data to ThreatIntelligence"""
        ip = host.get("ip_str", "unknown")
        vulns = host.get("vulns", [])
        tags = host.get("tags", [])
        
        # Determine severity based on vulnerabilities and tags
        severity = ThreatSeverity.LOW
        if vulns:
            severity = ThreatSeverity.HIGH if len(vulns) > 2 else ThreatSeverity.MEDIUM
        if "malware" in tags or "botnet" in tags:
            severity = ThreatSeverity.CRITICAL
        
        # Create indicators
        indicators = [
            ThreatIndicator(
                type="ip",
                value=ip,
                confidence=80,
                first_seen=datetime.utcnow(),
                last_seen=datetime.utcnow(),
                tags=tags
            )
        ]
        
        # Add vulnerability indicators
        for vuln in vulns[:5]:
            indicators.append(
                ThreatIndicator(
                    type="cve",
                    value=vuln,
                    confidence=90,
                    first_seen=datetime.utcnow(),
                    last_seen=datetime.utcnow()
                )
            )
        
        # Create geo location
        geo_location = None
        if host.get("country_code"):
            geo_location = GeoLocation(
                country=host.get("country_name"),
                country_code=host.get("country_code"),
                city=host.get("city"),
                region=host.get("region_code"),
                latitude=host.get("latitude"),
                longitude=host.get("longitude")
            )
        
        # Generate title and description
        title = f"{threat_type.value.title()} detected: {ip}"
        description = f"Host {ip} identified with {len(vulns)} vulnerabilities"
        if host.get("org"):
            description += f" (Organization: {host['org']})"
        
        return ThreatIntelligence(
            threat_id=f"threat-{uuid.uuid4()}",
            threat_type=threat_type,
            severity=severity,
            status=ThreatStatus.ACTIVE,
            title=title,
            description=description,
            indicators=indicators,
            affected_systems=[host.get("os", "Unknown")] if host.get("os") else [],
            attack_vector="Network scanning" if threat_type == ThreatType.VULNERABILITY else "Unknown",
            mitigation=f"Block IP {ip}, patch vulnerabilities" if vulns else f"Monitor IP {ip}",
            references=[],
            geo_location=geo_location,
            source="Shodan",
            confidence_score=85 if vulns else 70,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            metadata={
                "ports": host.get("ports", []),
                "hostnames": host.get("hostnames", []),
                "isp": host.get("isp"),
                "asn": host.get("asn")
            }
        )
    
    async def _store_threat(self, threat: ThreatIntelligence):
        """Store threat in database"""
        try:
            db = cast(Any, get_database())
            await db.threat_intelligence.insert_one(threat.model_dump(mode='json'))
            logger.info(f"Stored threat: {threat.threat_id}")
        except Exception as e:
            logger.error(f"Failed to store threat: {e}")
    
    async def update_threat_status(self, threat_id: str, status: ThreatStatus) -> bool:
        """Update threat status"""
        try:
            db = cast(Any, get_database())
            result = await db.threat_intelligence.update_one(
                {"threat_id": threat_id},
                {"$set": {"status": status.value, "updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to update threat status: {e}")
            return False


# Made with Bob