"""
Incident Report Service
AI-powered incident report generation and management
"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.report import (
    IncidentReport, ReportGenerationRequest, ReportSearchRequest,
    ReportListResponse, ReportUpdateRequest, IncidentSeverity,
    IncidentType, IncidentStatus, AttackVector, AffectedSystem,
    TimelineEvent, MitigationStep, IncidentIndicator
)
from app.services.ai_service import AIService
from app.database.mongodb import get_database

logger = logging.getLogger(__name__)


class ReportService:
    """Service for generating and managing incident reports"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.collection_name = "incident_reports"
    
    async def generate_report(self, request: ReportGenerationRequest) -> IncidentReport:
        """
        Generate a comprehensive incident report using AI
        
        Args:
            request: Report generation request with incident details
            
        Returns:
            Generated incident report
        """
        logger.info(f"Generating incident report: {request.title}")
        
        # Generate report ID
        report_id = f"RPT-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        incident_id = request.incident_id or f"INC-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        # Generate AI-powered content
        ai_content = await self._generate_ai_content(request)
        
        # Parse affected systems
        affected_systems = self._parse_affected_systems(
            request.affected_systems_info or []
        )
        
        # Parse indicators
        indicators = self._parse_indicators(
            request.indicators_info or []
        )
        
        # Generate attack vectors with MITRE mapping
        attack_vectors = []
        if request.include_mitre_mapping:
            attack_vectors = self._generate_attack_vectors(
                request.incident_type,
                request.description
            )
        
        # Generate timeline
        timeline = self._generate_timeline(
            request.detection_time or datetime.utcnow(),
            request.incident_type
        )
        
        # Generate mitigation steps
        mitigation_steps = self._generate_mitigation_steps(
            request.incident_type,
            request.severity
        )
        
        # Generate recommendations
        recommendations = []
        if request.include_recommendations:
            recommendations = self._generate_recommendations(
                request.incident_type,
                request.severity
            )
        
        # Create the report
        report = IncidentReport(
            report_id=report_id,
            incident_id=incident_id,
            title=request.title,
            incident_type=request.incident_type,
            severity=request.severity,
            status=IncidentStatus.INVESTIGATING,
            executive_summary=ai_content["executive_summary"],
            detection_time=request.detection_time or datetime.utcnow(),
            start_time=request.detection_time,
            end_time=None,
            attack_vectors=attack_vectors,
            affected_systems=affected_systems,
            indicators=indicators,
            timeline=timeline,
            mitigation_steps=mitigation_steps,
            recommendations=recommendations,
            impact_description=ai_content["impact_description"],
            data_compromised=self._assess_data_compromise(request.incident_type),
            estimated_cost=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            created_by="AI System",
            additional_notes=None
        )
        
        # Store in database
        await self._store_report(report)
        
        logger.info(f"Generated report {report_id} for incident {incident_id}")
        return report
    
    async def _generate_ai_content(self, request: ReportGenerationRequest) -> Dict[str, str]:
        """Generate AI-powered content for the report"""
        
        # Create prompt for AI
        prompt = f"""Generate a comprehensive incident report for the following security incident:

Title: {request.title}
Type: {request.incident_type.value}
Severity: {request.severity.value}
Description: {request.description}

Please provide:
1. Executive Summary (2-3 paragraphs for C-level executives)
2. Impact Description (detailed technical impact assessment)

Format the response as JSON with keys: executive_summary, impact_description"""
        
        try:
            # Use AI service to generate content
            ai_response = await self.ai_service.generate_incident_report_content(
                prompt=prompt
            )
            
            # Parse AI response
            if isinstance(ai_response, dict):
                return {
                    "executive_summary": ai_response.get("executive_summary", self._get_default_summary(request)),
                    "impact_description": ai_response.get("impact_description", self._get_default_impact(request))
                }
            else:
                # Fallback to default content
                return {
                    "executive_summary": self._get_default_summary(request),
                    "impact_description": self._get_default_impact(request)
                }
        except Exception as e:
            logger.error(f"AI content generation failed: {e}")
            return {
                "executive_summary": self._get_default_summary(request),
                "impact_description": self._get_default_impact(request)
            }
    
    def _get_default_summary(self, request: ReportGenerationRequest) -> str:
        """Generate default executive summary"""
        return f"""A {request.severity.value} severity {request.incident_type.value} incident was detected and is currently under investigation. {request.description}

The incident response team has been activated and is working to contain the threat, assess the full scope of the impact, and implement appropriate remediation measures. Initial analysis suggests this incident requires immediate attention and coordinated response efforts.

This report provides a comprehensive overview of the incident, including technical details, affected systems, timeline of events, and recommended actions for mitigation and prevention of similar incidents in the future."""
    
    def _get_default_impact(self, request: ReportGenerationRequest) -> str:
        """Generate default impact description"""
        severity_impacts = {
            IncidentSeverity.CRITICAL: "severe disruption to business operations with potential for significant data loss or system compromise",
            IncidentSeverity.HIGH: "substantial impact on operations with potential for data exposure or system degradation",
            IncidentSeverity.MEDIUM: "moderate impact on operations with limited scope of affected systems",
            IncidentSeverity.LOW: "minimal impact on operations with isolated system effects",
            IncidentSeverity.INFORMATIONAL: "no immediate operational impact but requires monitoring"
        }
        
        return f"""This {request.incident_type.value} incident has resulted in {severity_impacts.get(request.severity, 'impact on operations')}. The affected systems have been identified and are being monitored closely. Initial assessment indicates that immediate containment measures are necessary to prevent further spread or escalation of the incident."""
    
    def _parse_affected_systems(self, systems_info: List[str]) -> List[AffectedSystem]:
        """Parse affected systems information"""
        affected_systems = []
        for i, system_info in enumerate(systems_info[:10]):  # Limit to 10 systems
            affected_systems.append(AffectedSystem(
                system_name=system_info,
                system_type="Server" if "SERVER" in system_info.upper() else "Workstation",
                ip_address=None,
                impact_level="High" if i < 3 else "Medium",
                compromised=i < 2  # First 2 systems marked as compromised
            ))
        return affected_systems
    
    def _parse_indicators(self, indicators_info: List[str]) -> List[IncidentIndicator]:
        """Parse indicators of compromise"""
        indicators = []
        for indicator_info in indicators_info[:20]:  # Limit to 20 indicators
            # Determine indicator type
            if "." in indicator_info and indicator_info.count(".") == 3:
                indicator_type = "IP Address"
            elif "." in indicator_info and not indicator_info.count(".") == 3:
                indicator_type = "Domain"
            elif len(indicator_info) in [32, 40, 64]:
                indicator_type = "File Hash"
            else:
                indicator_type = "Other"
            
            indicators.append(IncidentIndicator(
                indicator_type=indicator_type,
                value=indicator_info,
                description=None,
                confidence=85
            ))
        return indicators
    
    def _generate_attack_vectors(self, incident_type: IncidentType, description: str) -> List[AttackVector]:
        """Generate attack vectors with MITRE ATT&CK mapping"""
        
        # MITRE ATT&CK mappings for common incident types
        mitre_mappings = {
            IncidentType.PHISHING: [
                AttackVector(
                    vector_type="Spear Phishing Attachment",
                    description="Targeted email with malicious attachment",
                    mitre_technique="T1566.001",
                    mitre_tactic="Initial Access"
                ),
                AttackVector(
                    vector_type="User Execution",
                    description="User opened malicious attachment",
                    mitre_technique="T1204.002",
                    mitre_tactic="Execution"
                )
            ],
            IncidentType.MALWARE: [
                AttackVector(
                    vector_type="Malicious File",
                    description="Execution of malicious executable",
                    mitre_technique="T1204.002",
                    mitre_tactic="Execution"
                ),
                AttackVector(
                    vector_type="Command and Control",
                    description="Communication with C2 server",
                    mitre_technique="T1071.001",
                    mitre_tactic="Command and Control"
                )
            ],
            IncidentType.RANSOMWARE: [
                AttackVector(
                    vector_type="Data Encrypted for Impact",
                    description="Files encrypted by ransomware",
                    mitre_technique="T1486",
                    mitre_tactic="Impact"
                ),
                AttackVector(
                    vector_type="Inhibit System Recovery",
                    description="Deletion of backup files",
                    mitre_technique="T1490",
                    mitre_tactic="Impact"
                )
            ],
            IncidentType.DATA_BREACH: [
                AttackVector(
                    vector_type="Data from Local System",
                    description="Unauthorized data access",
                    mitre_technique="T1005",
                    mitre_tactic="Collection"
                ),
                AttackVector(
                    vector_type="Exfiltration Over C2 Channel",
                    description="Data exfiltration",
                    mitre_technique="T1041",
                    mitre_tactic="Exfiltration"
                )
            ],
            IncidentType.UNAUTHORIZED_ACCESS: [
                AttackVector(
                    vector_type="Valid Accounts",
                    description="Use of compromised credentials",
                    mitre_technique="T1078",
                    mitre_tactic="Initial Access"
                ),
                AttackVector(
                    vector_type="Brute Force",
                    description="Password guessing attack",
                    mitre_technique="T1110",
                    mitre_tactic="Credential Access"
                )
            ]
        }
        
        return mitre_mappings.get(incident_type, [
            AttackVector(
                vector_type="Unknown",
                description="Attack vector under investigation",
                mitre_technique=None,
                mitre_tactic="Unknown"
            )
        ])
    
    def _generate_timeline(self, detection_time: datetime, incident_type: IncidentType) -> List[TimelineEvent]:
        """Generate incident timeline"""
        timeline = [
            TimelineEvent(
                timestamp=detection_time,
                event_type="Initial Detection",
                description=f"{incident_type.value.replace('_', ' ').title()} activity detected by security monitoring systems",
                source="Security Operations Center"
            )
        ]
        return timeline
    
    def _generate_mitigation_steps(self, incident_type: IncidentType, severity: IncidentSeverity) -> List[MitigationStep]:
        """Generate mitigation steps based on incident type"""
        
        common_steps = [
            MitigationStep(
                step_number=1,
                action="Isolate affected systems from the network",
                status="In Progress",
                assigned_to="SOC Team",
                completed_at=None
            ),
            MitigationStep(
                step_number=2,
                action="Preserve evidence for forensic analysis",
                status="Pending",
                assigned_to="Forensics Team",
                completed_at=None
            ),
            MitigationStep(
                step_number=3,
                action="Identify and contain the threat",
                status="Pending",
                assigned_to="Incident Response Team",
                completed_at=None
            )
        ]
        
        # Add incident-specific steps
        if incident_type == IncidentType.RANSOMWARE:
            common_steps.append(MitigationStep(
                step_number=4,
                action="Restore systems from clean backups",
                status="Pending",
                assigned_to="IT Operations",
                completed_at=None
            ))
        elif incident_type == IncidentType.PHISHING:
            common_steps.append(MitigationStep(
                step_number=4,
                action="Block malicious email addresses and domains",
                status="Pending",
                assigned_to="Email Security Team",
                completed_at=None
            ))
        elif incident_type == IncidentType.DATA_BREACH:
            common_steps.append(MitigationStep(
                step_number=4,
                action="Assess scope of data exposure",
                status="Pending",
                assigned_to="Data Protection Team",
                completed_at=None
            ))
        
        return common_steps
    
    def _generate_recommendations(self, incident_type: IncidentType, severity: IncidentSeverity) -> List[str]:
        """Generate recommendations for prevention"""
        
        common_recommendations = [
            "Conduct comprehensive security awareness training for all employees",
            "Implement multi-factor authentication across all systems",
            "Regularly update and patch all systems and applications",
            "Enhance monitoring and logging capabilities",
            "Conduct regular security assessments and penetration testing"
        ]
        
        # Add incident-specific recommendations
        specific_recommendations = {
            IncidentType.PHISHING: [
                "Deploy advanced email filtering and anti-phishing solutions",
                "Implement DMARC, SPF, and DKIM email authentication",
                "Conduct regular phishing simulation exercises"
            ],
            IncidentType.RANSOMWARE: [
                "Implement robust backup and recovery procedures",
                "Deploy endpoint detection and response (EDR) solutions",
                "Segment network to limit lateral movement"
            ],
            IncidentType.DATA_BREACH: [
                "Implement data loss prevention (DLP) solutions",
                "Encrypt sensitive data at rest and in transit",
                "Conduct regular access reviews and implement least privilege"
            ]
        }
        
        recommendations = common_recommendations.copy()
        if incident_type in specific_recommendations:
            recommendations.extend(specific_recommendations[incident_type])
        
        return recommendations[:8]  # Limit to 8 recommendations
    
    def _assess_data_compromise(self, incident_type: IncidentType) -> bool:
        """Assess if data was likely compromised"""
        data_compromise_types = [
            IncidentType.DATA_BREACH,
            IncidentType.RANSOMWARE,
            IncidentType.APT
        ]
        return incident_type in data_compromise_types
    
    async def _store_report(self, report: IncidentReport) -> None:
        """Store report in database"""
        try:
            db: Any = get_database()
            collection = db[self.collection_name]
            
            report_dict = report.model_dump()
            await collection.insert_one(report_dict)
            
            logger.info(f"Stored report {report.report_id} in database")
        except Exception as e:
            logger.error(f"Failed to store report: {e}")
            raise
    
    async def get_report(self, report_id: str) -> Optional[IncidentReport]:
        """Get a specific report by ID"""
        try:
            db: Any = get_database()
            collection = db[self.collection_name]
            
            report_dict = await collection.find_one({"report_id": report_id})
            if report_dict:
                report_dict.pop("_id", None)
                return IncidentReport(**report_dict)
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve report {report_id}: {e}")
            return None
    
    async def search_reports(self, request: ReportSearchRequest) -> ReportListResponse:
        """Search reports with filters"""
        try:
            db: Any = get_database()
            collection = db[self.collection_name]
            
            # Build query
            query: Dict[str, Any] = {}
            
            if request.incident_type:
                query["incident_type"] = request.incident_type.value
            
            if request.severity:
                query["severity"] = request.severity.value
            
            if request.status:
                query["status"] = request.status.value
            
            if request.start_date or request.end_date:
                date_query: Dict[str, Any] = {}
                if request.start_date:
                    date_query["$gte"] = request.start_date
                if request.end_date:
                    date_query["$lte"] = request.end_date
                query["detection_time"] = date_query
            
            if request.search_text:
                query["$or"] = [
                    {"title": {"$regex": request.search_text, "$options": "i"}},
                    {"executive_summary": {"$regex": request.search_text, "$options": "i"}}
                ]
            
            # Get total count
            total = await collection.count_documents(query)
            
            # Get reports
            cursor = collection.find(query).sort("created_at", -1).skip(request.skip).limit(request.limit)
            reports = []
            
            async for report_dict in cursor:
                report_dict.pop("_id", None)
                reports.append(IncidentReport(**report_dict))
            
            return ReportListResponse(
                reports=reports,
                total=total,
                skip=request.skip,
                limit=request.limit
            )
        except Exception as e:
            logger.error(f"Failed to search reports: {e}")
            return ReportListResponse(reports=[], total=0, skip=0, limit=request.limit)
    
    async def update_report(self, report_id: str, update: ReportUpdateRequest) -> Optional[IncidentReport]:
        """Update an existing report"""
        try:
            db: Any = get_database()
            collection = db[self.collection_name]
            
            # Build update document
            update_doc: Dict[str, Any] = {"updated_at": datetime.utcnow()}
            
            if update.status:
                update_doc["status"] = update.status.value
            
            if update.additional_notes:
                update_doc["additional_notes"] = update.additional_notes
            
            if update.mitigation_steps:
                update_doc["mitigation_steps"] = [step.model_dump() for step in update.mitigation_steps]
            
            if update.recommendations:
                update_doc["recommendations"] = update.recommendations
            
            # Update in database
            result = await collection.update_one(
                {"report_id": report_id},
                {"$set": update_doc}
            )
            
            if result.modified_count > 0:
                return await self.get_report(report_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update report {report_id}: {e}")
            return None
    
    async def delete_report(self, report_id: str) -> bool:
        """Delete a report"""
        try:
            db: Any = get_database()
            collection = db[self.collection_name]
            
            result = await collection.delete_one({"report_id": report_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete report {report_id}: {e}")
            return False

# Made with Bob
