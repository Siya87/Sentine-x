"""
OSINT Investigation Models
Data models for OSINT investigations
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class InvestigationType(str, Enum):
    """Types of OSINT investigations"""
    USERNAME = "username"
    EMAIL = "email"
    PHONE = "phone"
    DOMAIN = "domain"
    IP_ADDRESS = "ip_address"


class RiskLevel(str, Enum):
    """Risk level classifications"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DataSource(BaseModel):
    """Information about a data source"""
    name: str
    url: Optional[str] = None
    found: bool
    data: Optional[Dict[str, Any]] = None
    last_seen: Optional[str] = None


class BreachInfo(BaseModel):
    """Data breach information"""
    breach_name: str
    breach_date: Optional[str] = None
    compromised_data: List[str] = []
    description: Optional[str] = None
    verified: bool = False


class SocialProfile(BaseModel):
    """Social media profile information"""
    platform: str
    username: str
    url: str
    followers: Optional[int] = None
    verified: bool = False
    last_activity: Optional[str] = None


class DomainInfo(BaseModel):
    """Domain information"""
    domain: str
    registrar: Optional[str] = None
    creation_date: Optional[str] = None
    expiration_date: Optional[str] = None
    name_servers: List[str] = []
    status: Optional[str] = None


class IPInfo(BaseModel):
    """IP address information"""
    ip: str
    country: Optional[str] = None
    city: Optional[str] = None
    isp: Optional[str] = None
    abuse_score: Optional[int] = None
    is_vpn: bool = False
    is_proxy: bool = False


class OSINTInvestigationRequest(BaseModel):
    """Request model for OSINT investigation"""
    investigation_type: InvestigationType
    target: str = Field(..., description="Target to investigate (username, email, phone, domain, or IP)")
    deep_scan: bool = Field(default=False, description="Perform deep scan (slower but more thorough)")
    include_breaches: bool = Field(default=True, description="Check for data breaches")
    include_social: bool = Field(default=True, description="Search social media profiles")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "investigation_type": "email",
                "target": "suspect@example.com",
                "deep_scan": True,
                "include_breaches": True,
                "include_social": True
            }
        }


class OSINTInvestigationResponse(BaseModel):
    """Response model for OSINT investigation"""
    investigation_id: str
    investigation_type: InvestigationType
    target: str
    risk_level: RiskLevel
    risk_score: int = Field(..., ge=0, le=100, description="Risk score from 0-100")
    
    # Investigation results
    data_sources: List[DataSource] = []
    breaches: List[BreachInfo] = []
    social_profiles: List[SocialProfile] = []
    domain_info: Optional[DomainInfo] = None
    ip_info: Optional[IPInfo] = None
    
    # Analysis
    summary: str
    findings: List[str] = []
    recommendations: List[str] = []
    
    # Metadata
    sources_checked: int
    sources_found: int
    created_at: datetime
    scan_duration: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "investigation_id": "osint-550e8400-e29b-41d4-a716-446655440000",
                "investigation_type": "email",
                "target": "suspect@example.com",
                "risk_level": "high",
                "risk_score": 75,
                "data_sources": [
                    {
                        "name": "HaveIBeenPwned",
                        "found": True,
                        "data": {"breaches": 3}
                    }
                ],
                "breaches": [
                    {
                        "breach_name": "LinkedIn",
                        "breach_date": "2021-06-01",
                        "compromised_data": ["email", "password"],
                        "verified": True
                    }
                ],
                "social_profiles": [
                    {
                        "platform": "Twitter",
                        "username": "suspect",
                        "url": "https://twitter.com/suspect",
                        "verified": False
                    }
                ],
                "summary": "Email found in 3 data breaches. Active on 2 social platforms.",
                "findings": [
                    "Email compromised in LinkedIn breach (2021)",
                    "Active Twitter account with suspicious activity",
                    "Email associated with multiple online services"
                ],
                "recommendations": [
                    "Change passwords for all associated accounts",
                    "Enable two-factor authentication",
                    "Monitor for suspicious activity"
                ],
                "sources_checked": 10,
                "sources_found": 5,
                "created_at": "2026-05-02T03:45:00Z",
                "scan_duration": 2.5
            }
        }


class OSINTInvestigationListResponse(BaseModel):
    """Response model for list of investigations"""
    total: int
    investigations: List[OSINTInvestigationResponse]


class OSINTStatsResponse(BaseModel):
    """Response model for OSINT statistics"""
    total_investigations: int
    by_type: Dict[str, int]
    by_risk_level: Dict[str, int]
    avg_risk_score: float
    total_breaches_found: int
    total_social_profiles_found: int

# Made with Bob
