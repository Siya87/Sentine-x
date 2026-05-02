"""
Pydantic models for Phishing Detection feature
"""
from pydantic import BaseModel, validator, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class PhishingIndicator(BaseModel):
    """Phishing indicator model"""
    type: str = Field(..., description="Type of indicator (urgency, spoofing, etc.)")
    description: str = Field(..., description="Detailed description")
    severity: str = Field(..., description="Severity level: low, medium, high, critical")


class PhishingAnalysisRequest(BaseModel):
    """Request model for phishing analysis"""
    content_type: str = Field(..., description="Type: email, url, sms, file")
    content: str = Field(..., description="Content to analyze")
    sender: Optional[str] = Field(None, description="Sender email or identifier")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    @validator('content_type')
    def validate_content_type(cls, v):
        """Validate content type"""
        allowed = ['email', 'url', 'sms', 'file']
        if v not in allowed:
            raise ValueError(f'content_type must be one of {allowed}')
        return v
    
    @validator('content')
    def validate_content(cls, v):
        """Validate content length"""
        if not v or len(v.strip()) == 0:
            raise ValueError('content cannot be empty')
        if len(v) > 1_000_000:  # 1MB limit
            raise ValueError('content too large (max 1MB)')
        return v


class PhishingAnalysisResponse(BaseModel):
    """Response model for phishing analysis"""
    analysis_id: str = Field(..., description="Unique analysis ID")
    threat_score: int = Field(..., ge=0, le=100, description="Threat score 0-100")
    is_phishing: bool = Field(..., description="Whether content is phishing")
    confidence: int = Field(..., ge=0, le=100, description="Confidence level 0-100")
    indicators: List[PhishingIndicator] = Field(..., description="List of indicators found")
    explanation: str = Field(..., description="Detailed explanation")
    recommendations: List[str] = Field(..., description="Recommended actions")
    virustotal_results: Optional[Dict[str, Any]] = Field(None, description="VirusTotal scan results")
    created_at: datetime = Field(..., description="Analysis timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
                "threat_score": 85,
                "is_phishing": True,
                "confidence": 90,
                "indicators": [
                    {
                        "type": "urgency",
                        "description": "Content contains urgent language",
                        "severity": "high"
                    }
                ],
                "explanation": "This appears to be a phishing attempt...",
                "recommendations": [
                    "Do not click any links",
                    "Report to security team"
                ],
                "virustotal_results": None,
                "created_at": "2026-05-01T19:00:00Z"
            }
        }


class PhishingAnalysisListResponse(BaseModel):
    """Response model for list of analyses"""
    total: int = Field(..., description="Total number of analyses")
    analyses: List[PhishingAnalysisResponse] = Field(..., description="List of analyses")


class PhishingAnalysisDetail(BaseModel):
    """Detailed analysis model with full content"""
    analysis_id: str
    content_type: str
    content: str
    sender: Optional[str]
    urls_found: List[str]
    threat_score: int
    is_phishing: bool
    confidence: int
    indicators: List[PhishingIndicator]
    explanation: str
    recommendations: List[str]
    virustotal_results: Optional[Dict[str, Any]]
    created_at: datetime
    status: str = Field(..., description="Analysis status: pending, completed, failed")

# Made with Bob
