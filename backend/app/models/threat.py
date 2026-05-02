"""
Threat Intelligence Data Models
Pydantic models for threat intelligence dashboard
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ThreatType(str, Enum):
    """Types of threats"""
    MALWARE = "malware"
    PHISHING = "phishing"
    RANSOMWARE = "ransomware"
    BOTNET = "botnet"
    DDOS = "ddos"
    EXPLOIT = "exploit"
    VULNERABILITY = "vulnerability"
    SUSPICIOUS_IP = "suspicious_ip"
    MALICIOUS_DOMAIN = "malicious_domain"
    DATA_BREACH = "data_breach"


class ThreatSeverity(str, Enum):
    """Threat severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThreatStatus(str, Enum):
    """Threat status"""
    ACTIVE = "active"
    MITIGATED = "mitigated"
    MONITORING = "monitoring"
    RESOLVED = "resolved"


class GeoLocation(BaseModel):
    """Geographic location data"""
    country: Optional[str] = None
    country_code: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "country": "United States",
                "country_code": "US",
                "city": "New York",
                "region": "New York",
                "latitude": 40.7128,
                "longitude": -74.0060
            }
        }


class ThreatIndicator(BaseModel):
    """Threat indicator (IOC)"""
    type: str = Field(..., description="Indicator type (ip, domain, hash, url)")
    value: str = Field(..., description="Indicator value")
    confidence: int = Field(..., ge=0, le=100, description="Confidence score 0-100")
    first_seen: datetime = Field(default_factory=datetime.utcnow)
    last_seen: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "ip",
                "value": "192.168.1.1",
                "confidence": 85,
                "first_seen": "2024-01-01T00:00:00Z",
                "last_seen": "2024-01-15T12:00:00Z",
                "tags": ["malware", "c2"]
            }
        }


class ThreatIntelligence(BaseModel):
    """Threat intelligence entry"""
    threat_id: str = Field(..., description="Unique threat identifier")
    threat_type: ThreatType
    severity: ThreatSeverity
    status: ThreatStatus = ThreatStatus.ACTIVE
    title: str = Field(..., description="Threat title")
    description: str = Field(..., description="Detailed description")
    indicators: List[ThreatIndicator] = Field(default_factory=list)
    affected_systems: List[str] = Field(default_factory=list)
    attack_vector: Optional[str] = None
    mitigation: Optional[str] = None
    references: List[str] = Field(default_factory=list)
    geo_location: Optional[GeoLocation] = None
    source: str = Field(..., description="Intelligence source")
    confidence_score: int = Field(..., ge=0, le=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "threat_id": "threat-12345",
                "threat_type": "malware",
                "severity": "high",
                "status": "active",
                "title": "New Ransomware Campaign Detected",
                "description": "A new ransomware variant targeting healthcare organizations",
                "indicators": [
                    {
                        "type": "ip",
                        "value": "192.168.1.100",
                        "confidence": 90,
                        "tags": ["ransomware", "c2"]
                    }
                ],
                "affected_systems": ["Windows 10", "Windows Server 2019"],
                "attack_vector": "Phishing email with malicious attachment",
                "mitigation": "Block IP addresses, update antivirus signatures",
                "references": ["https://example.com/threat-report"],
                "source": "Shodan",
                "confidence_score": 85,
                "created_at": "2024-01-01T00:00:00Z"
            }
        }


class ThreatStatistics(BaseModel):
    """Threat statistics"""
    total_threats: int = 0
    active_threats: int = 0
    critical_threats: int = 0
    high_threats: int = 0
    medium_threats: int = 0
    low_threats: int = 0
    by_type: Dict[str, int] = Field(default_factory=dict)
    by_country: Dict[str, int] = Field(default_factory=dict)
    recent_threats: List[ThreatIntelligence] = Field(default_factory=list)
    trending_indicators: List[ThreatIndicator] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_threats": 150,
                "active_threats": 45,
                "critical_threats": 12,
                "high_threats": 28,
                "medium_threats": 65,
                "low_threats": 45,
                "by_type": {
                    "malware": 50,
                    "phishing": 30,
                    "ransomware": 20
                },
                "by_country": {
                    "US": 40,
                    "CN": 30,
                    "RU": 25
                }
            }
        }


class ThreatSearchRequest(BaseModel):
    """Threat search request"""
    query: Optional[str] = Field(None, description="Search query")
    threat_type: Optional[ThreatType] = None
    severity: Optional[ThreatSeverity] = None
    status: Optional[ThreatStatus] = None
    country: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(default=50, ge=1, le=1000)
    skip: int = Field(default=0, ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "ransomware",
                "threat_type": "malware",
                "severity": "high",
                "status": "active",
                "limit": 20,
                "skip": 0
            }
        }


class ThreatSearchResponse(BaseModel):
    """Threat search response"""
    total: int
    threats: List[ThreatIntelligence]
    page: int
    page_size: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "total": 150,
                "threats": [],
                "page": 1,
                "page_size": 20
            }
        }


class ShodanHostInfo(BaseModel):
    """Shodan host information"""
    ip: str
    hostnames: List[str] = Field(default_factory=list)
    domains: List[str] = Field(default_factory=list)
    ports: List[int] = Field(default_factory=list)
    vulns: List[str] = Field(default_factory=list)
    os: Optional[str] = None
    organization: Optional[str] = None
    isp: Optional[str] = None
    asn: Optional[str] = None
    country_code: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    last_update: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "ip": "8.8.8.8",
                "hostnames": ["dns.google"],
                "domains": ["google.com"],
                "ports": [53, 443],
                "vulns": [],
                "os": "Linux",
                "organization": "Google LLC",
                "isp": "Google",
                "country_code": "US",
                "city": "Mountain View"
            }
        }


class ThreatFeedRequest(BaseModel):
    """Real-time threat feed request"""
    feed_type: str = Field(..., description="Type of feed (malware, phishing, etc)")
    limit: int = Field(default=100, ge=1, le=1000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "feed_type": "malware",
                "limit": 50
            }
        }


# Made with Bob