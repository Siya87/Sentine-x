"""
Threat Intelligence API Routes
Endpoints for threat intelligence dashboard
"""
from fastapi import APIRouter, HTTPException, Query
from app.models.threat import (
    ThreatIntelligence,
    ThreatSearchRequest,
    ThreatSearchResponse,
    ThreatStatistics,
    ShodanHostInfo,
    ThreatStatus
)
from app.services.threat_service import ThreatService
import logging
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter()
threat_service = ThreatService()


@router.get("/live", response_model=list[ThreatIntelligence])
async def get_live_threats(
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of threats to return")
):
    """
    Get live threat intelligence from multiple sources
    
    Returns real-time threat data aggregated from:
    - Shodan (malware C2, ransomware, vulnerabilities)
    - AbuseIPDB (malicious IPs)
    - Internal threat database
    
    **Response includes:**
    - Threat type and severity
    - Geographic location
    - Indicators of Compromise (IOCs)
    - Mitigation recommendations
    """
    try:
        logger.info(f"Fetching {limit} live threats")
        threats = await threat_service.get_live_threats(limit=limit)
        return threats
    except Exception as e:
        logger.error(f"Failed to get live threats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve threats: {str(e)}")


@router.post("/search", response_model=ThreatSearchResponse)
async def search_threats(request: ThreatSearchRequest):
    """
    Search threats with advanced filters
    
    **Filters available:**
    - Query text (searches title and description)
    - Threat type (malware, phishing, ransomware, etc.)
    - Severity level (low, medium, high, critical)
    - Status (active, mitigated, monitoring, resolved)
    - Country code
    - Date range
    
    **Returns:**
    - Paginated list of matching threats
    - Total count
    - Page information
    """
    try:
        logger.info(f"Searching threats with filters: {request.model_dump()}")
        
        threats, total = await threat_service.search_threats(
            query=request.query,
            threat_type=request.threat_type,
            severity=request.severity,
            status=request.status,
            country=request.country,
            start_date=request.start_date,
            end_date=request.end_date,
            limit=request.limit,
            skip=request.skip
        )
        
        page = (request.skip // request.limit) + 1
        
        return ThreatSearchResponse(
            total=total,
            threats=threats,
            page=page,
            page_size=request.limit
        )
        
    except Exception as e:
        logger.error(f"Threat search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/{threat_id}", response_model=ThreatIntelligence)
async def get_threat(threat_id: str):
    """
    Get detailed information about a specific threat
    
    **Returns:**
    - Complete threat details
    - All indicators of compromise
    - Geographic information
    - Mitigation steps
    - Related references
    """
    try:
        logger.info(f"Fetching threat: {threat_id}")
        threat = await threat_service.get_threat_by_id(threat_id)
        
        if not threat:
            raise HTTPException(status_code=404, detail="Threat not found")
        
        return threat
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get threat: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve threat: {str(e)}")


@router.get("/stats/summary", response_model=ThreatStatistics)
async def get_threat_statistics():
    """
    Get comprehensive threat statistics
    
    **Returns:**
    - Total threats count
    - Active threats count
    - Breakdown by severity (critical, high, medium, low)
    - Breakdown by threat type
    - Breakdown by country
    - Recent threats (last 10)
    - Trending indicators
    
    **Use cases:**
    - Dashboard overview
    - Executive reporting
    - Trend analysis
    """
    try:
        logger.info("Fetching threat statistics")
        stats = await threat_service.get_statistics()
        return stats
        
    except Exception as e:
        logger.error(f"Failed to get statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve statistics: {str(e)}")


@router.get("/host/{ip}", response_model=ShodanHostInfo)
async def get_host_info(ip: str):
    """
    Get detailed host information from Shodan
    
    **Returns:**
    - IP address and hostnames
    - Open ports and services
    - Known vulnerabilities
    - Organization and ISP
    - Geographic location
    - Last update timestamp
    
    **Use cases:**
    - Threat investigation
    - Asset discovery
    - Vulnerability assessment
    """
    try:
        logger.info(f"Fetching host info for: {ip}")
        host_info = await threat_service.get_host_info(ip)
        
        if not host_info:
            raise HTTPException(status_code=404, detail="Host information not found")
        
        return host_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get host info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve host info: {str(e)}")


@router.get("/country/{country_code}", response_model=list[ThreatIntelligence])
async def get_country_threats(
    country_code: str,
    limit: int = Query(default=50, ge=1, le=500, description="Maximum number of threats")
):
    """
    Get threats originating from a specific country
    
    **Parameters:**
    - country_code: Two-letter ISO country code (e.g., US, CN, RU)
    - limit: Maximum number of results
    
    **Returns:**
    - List of threats from the specified country
    - Geographic distribution
    - Threat types prevalent in that region
    
    **Use cases:**
    - Geographic threat analysis
    - Regional security monitoring
    - Geopolitical threat intelligence
    """
    try:
        logger.info(f"Fetching threats from country: {country_code}")
        threats = await threat_service.get_country_threats(country_code, limit=limit)
        return threats
        
    except Exception as e:
        logger.error(f"Failed to get country threats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve country threats: {str(e)}")


@router.patch("/{threat_id}/status")
async def update_threat_status(
    threat_id: str,
    status: ThreatStatus
):
    """
    Update the status of a threat
    
    **Status options:**
    - active: Threat is currently active
    - mitigated: Threat has been mitigated
    - monitoring: Threat is being monitored
    - resolved: Threat has been resolved
    
    **Returns:**
    - Success message
    
    **Use cases:**
    - Incident response workflow
    - Threat lifecycle management
    - Status tracking
    """
    try:
        logger.info(f"Updating threat {threat_id} status to: {status}")
        success = await threat_service.update_threat_status(threat_id, status)
        
        if not success:
            raise HTTPException(status_code=404, detail="Threat not found or update failed")
        
        return {"message": "Threat status updated successfully", "threat_id": threat_id, "new_status": status}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update threat status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update status: {str(e)}")


# Made with Bob