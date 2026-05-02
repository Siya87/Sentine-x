"""
Incident Report Models
Data models for AI-generated incident reports
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class IncidentSeverity(str, Enum):
    """Incident severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class IncidentType(str, Enum):
    """Types of security incidents"""
    MALWARE = "malware"
    PHISHING = "phishing"
    DATA_BREACH = "data_breach"
    RANSOMWARE = "ransomware"
    DDOS = "ddos"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    INSIDER_THREAT = "insider_threat"
    APT = "apt"
    VULNERABILITY_EXPLOIT = "vulnerability_exploit"
    SOCIAL_ENGINEERING = "social_engineering"
    BOTNET = "botnet"
    CRYPTOJACKING = "cryptojacking"
    OTHER = "other"


class IncidentStatus(str, Enum):
    """Incident response status"""
    DETECTED = "detected"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    ERADICATED = "eradicated"
    RECOVERED = "recovered"
    CLOSED = "closed"


class AttackVector(BaseModel):
    """Attack vector information"""
    vector_type: str = Field(..., description="Type of attack vector")
    description: str = Field(..., description="Description of the attack vector")
    mitre_technique: Optional[str] = Field(None, description="MITRE ATT&CK technique ID")
    mitre_tactic: Optional[str] = Field(None, description="MITRE ATT&CK tactic")
    
    class Config:
        json_schema_extra = {
            "example": {
                "vector_type": "Spear Phishing",
                "description": "Targeted email with malicious attachment",
                "mitre_technique": "T1566.001",
                "mitre_tactic": "Initial Access"
            }
        }


class AffectedSystem(BaseModel):
    """Information about affected systems"""
    system_name: str = Field(..., description="Name or identifier of the system")
    system_type: str = Field(..., description="Type of system (server, workstation, etc.)")
    ip_address: Optional[str] = Field(None, description="IP address of the system")
    impact_level: str = Field(..., description="Level of impact on this system")
    compromised: bool = Field(False, description="Whether the system was compromised")
    
    class Config:
        json_schema_extra = {
            "example": {
                "system_name": "WEB-SERVER-01",
                "system_type": "Web Server",
                "ip_address": "192.168.1.100",
                "impact_level": "High",
                "compromised": True
            }
        }


class TimelineEvent(BaseModel):
    """Timeline event in the incident"""
    timestamp: datetime = Field(..., description="When the event occurred")
    event_type: str = Field(..., description="Type of event")
    description: str = Field(..., description="Description of what happened")
    source: Optional[str] = Field(None, description="Source of the event information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2024-01-15T10:30:00Z",
                "event_type": "Initial Detection",
                "description": "Suspicious network traffic detected by IDS",
                "source": "IDS Alert #12345"
            }
        }


class MitigationStep(BaseModel):
    """Mitigation or remediation step"""
    step_number: int = Field(..., description="Step number in sequence")
    action: str = Field(..., description="Action to be taken")
    status: str = Field(..., description="Status of this step")
    assigned_to: Optional[str] = Field(None, description="Person/team assigned")
    completed_at: Optional[datetime] = Field(None, description="When the step was completed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "step_number": 1,
                "action": "Isolate affected systems from network",
                "status": "Completed",
                "assigned_to": "SOC Team",
                "completed_at": "2024-01-15T11:00:00Z"
            }
        }


class IncidentIndicator(BaseModel):
    """Indicator of Compromise (IoC)"""
    indicator_type: str = Field(..., description="Type of indicator (IP, domain, hash, etc.)")
    value: str = Field(..., description="The indicator value")
    description: Optional[str] = Field(None, description="Description of the indicator")
    confidence: Optional[int] = Field(None, ge=0, le=100, description="Confidence level (0-100)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "indicator_type": "IP Address",
                "value": "192.168.1.50",
                "description": "Command and control server",
                "confidence": 95
            }
        }


class IncidentReport(BaseModel):
    """Complete incident report"""
    report_id: str = Field(..., description="Unique report identifier")
    incident_id: str = Field(..., description="Incident identifier")
    title: str = Field(..., description="Report title")
    incident_type: IncidentType = Field(..., description="Type of incident")
    severity: IncidentSeverity = Field(..., description="Incident severity")
    status: IncidentStatus = Field(..., description="Current incident status")
    
    # Executive Summary
    executive_summary: str = Field(..., description="High-level summary for executives")
    
    # Incident Details
    detection_time: datetime = Field(..., description="When the incident was detected")
    start_time: Optional[datetime] = Field(None, description="When the incident started")
    end_time: Optional[datetime] = Field(None, description="When the incident ended")
    
    # Technical Details
    attack_vectors: List[AttackVector] = Field(default_factory=list, description="Attack vectors used")
    affected_systems: List[AffectedSystem] = Field(default_factory=list, description="Systems affected")
    indicators: List[IncidentIndicator] = Field(default_factory=list, description="Indicators of compromise")
    
    # Timeline
    timeline: List[TimelineEvent] = Field(default_factory=list, description="Incident timeline")
    
    # Response
    mitigation_steps: List[MitigationStep] = Field(default_factory=list, description="Mitigation steps taken")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations for prevention")
    
    # Impact Assessment
    impact_description: str = Field(..., description="Description of the impact")
    data_compromised: bool = Field(False, description="Whether data was compromised")
    estimated_cost: Optional[float] = Field(None, description="Estimated cost of the incident")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Report creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update time")
    created_by: str = Field(default="AI System", description="Who created the report")
    
    # Additional Information
    additional_notes: Optional[str] = Field(None, description="Additional notes or observations")
    attachments: List[str] = Field(default_factory=list, description="List of attachment references")
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "RPT-2024-001",
                "incident_id": "INC-2024-001",
                "title": "Ransomware Attack on Production Systems",
                "incident_type": "ransomware",
                "severity": "critical",
                "status": "contained",
                "executive_summary": "A ransomware attack was detected on production systems...",
                "detection_time": "2024-01-15T10:30:00Z",
                "start_time": "2024-01-15T08:00:00Z",
                "impact_description": "Multiple production servers encrypted, services disrupted",
                "data_compromised": False,
                "created_at": "2024-01-15T12:00:00Z"
            }
        }


class ReportGenerationRequest(BaseModel):
    """Request to generate an incident report"""
    incident_id: Optional[str] = Field(None, description="Existing incident ID to generate report for")
    title: str = Field(..., description="Report title")
    incident_type: IncidentType = Field(..., description="Type of incident")
    severity: IncidentSeverity = Field(..., description="Incident severity")
    
    # Optional incident details
    description: str = Field(..., description="Detailed description of the incident")
    detection_time: Optional[datetime] = Field(None, description="When detected")
    affected_systems_info: Optional[List[str]] = Field(None, description="List of affected systems")
    indicators_info: Optional[List[str]] = Field(None, description="Known indicators")
    
    # AI generation preferences
    include_mitre_mapping: bool = Field(True, description="Include MITRE ATT&CK mapping")
    include_recommendations: bool = Field(True, description="Include recommendations")
    detail_level: str = Field("detailed", description="Level of detail: brief, standard, detailed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Phishing Campaign Targeting Finance Department",
                "incident_type": "phishing",
                "severity": "high",
                "description": "Multiple employees received phishing emails...",
                "detection_time": "2024-01-15T09:00:00Z",
                "affected_systems_info": ["MAIL-SERVER-01", "WORKSTATION-05"],
                "include_mitre_mapping": True,
                "detail_level": "detailed"
            }
        }


class ReportSearchRequest(BaseModel):
    """Request to search incident reports"""
    incident_type: Optional[IncidentType] = Field(None, description="Filter by incident type")
    severity: Optional[IncidentSeverity] = Field(None, description="Filter by severity")
    status: Optional[IncidentStatus] = Field(None, description="Filter by status")
    start_date: Optional[datetime] = Field(None, description="Filter by start date")
    end_date: Optional[datetime] = Field(None, description="Filter by end date")
    search_text: Optional[str] = Field(None, description="Search in title and description")
    limit: int = Field(10, ge=1, le=100, description="Maximum number of results")
    skip: int = Field(0, ge=0, description="Number of results to skip")
    
    class Config:
        json_schema_extra = {
            "example": {
                "incident_type": "phishing",
                "severity": "high",
                "start_date": "2024-01-01T00:00:00Z",
                "limit": 10
            }
        }


class ReportListResponse(BaseModel):
    """Response containing list of reports"""
    reports: List[IncidentReport] = Field(..., description="List of incident reports")
    total: int = Field(..., description="Total number of reports matching criteria")
    skip: int = Field(..., description="Number of results skipped")
    limit: int = Field(..., description="Maximum results returned")
    
    class Config:
        json_schema_extra = {
            "example": {
                "reports": [],
                "total": 25,
                "skip": 0,
                "limit": 10
            }
        }


class PDFExportRequest(BaseModel):
    """Request to export report as PDF"""
    report_id: str = Field(..., description="Report ID to export")
    include_attachments: bool = Field(False, description="Include attachments in PDF")
    template: str = Field("standard", description="PDF template to use")
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "RPT-2024-001",
                "include_attachments": False,
                "template": "standard"
            }
        }


class ReportUpdateRequest(BaseModel):
    """Request to update an existing report"""
    status: Optional[IncidentStatus] = Field(None, description="Update status")
    additional_notes: Optional[str] = Field(None, description="Add notes")
    mitigation_steps: Optional[List[MitigationStep]] = Field(None, description="Update mitigation steps")
    recommendations: Optional[List[str]] = Field(None, description="Update recommendations")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "closed",
                "additional_notes": "Incident fully resolved, all systems restored"
            }
        }

# Made with Bob
