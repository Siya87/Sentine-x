"""
OSINT Investigation API Routes
"""
from fastapi import APIRouter, HTTPException, Query
from app.models.osint import (
    OSINTInvestigationRequest,
    OSINTInvestigationResponse,
    OSINTInvestigationListResponse,
    OSINTStatsResponse
)
from app.services.osint_service import OSINTService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
osint_service = OSINTService()


@router.post("/investigate", response_model=OSINTInvestigationResponse)
async def investigate_target(request: OSINTInvestigationRequest):
    """
    Perform OSINT investigation on a target
    
    Supports investigation of:
    - Email addresses
    - Usernames
    - Phone numbers
    - Domain names
    - IP addresses
    
    Returns comprehensive intelligence including:
    - Data breach information
    - Social media profiles
    - IP reputation
    - Domain information
    - Risk assessment
    - AI-powered analysis
    """
    try:
        logger.info(f"Starting OSINT investigation for: {request.target}")
        result = await osint_service.investigate(request)
        return result
    except Exception as e:
        logger.error(f"OSINT investigation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Investigation failed: {str(e)}")


@router.get("/history", response_model=OSINTInvestigationListResponse)
async def get_investigation_history(
    limit: int = Query(default=10, ge=1, le=100, description="Number of results to return"),
    skip: int = Query(default=0, ge=0, description="Number of results to skip for pagination")
):
    """
    Get OSINT investigation history
    
    Returns a paginated list of previous investigations with:
    - Investigation details
    - Risk scores
    - Findings summary
    - Timestamps
    """
    try:
        investigations = await osint_service.get_investigation_history(limit=limit, skip=skip)
        return OSINTInvestigationListResponse(
            total=len(investigations),
            investigations=investigations
        )
    except Exception as e:
        logger.error(f"Failed to get investigation history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")


@router.get("/{investigation_id}", response_model=OSINTInvestigationResponse)
async def get_investigation(investigation_id: str):
    """
    Get specific OSINT investigation by ID
    
    Returns complete investigation details including:
    - All collected data
    - Risk assessment
    - Findings and recommendations
    - Source information
    """
    try:
        investigation = await osint_service.get_investigation(investigation_id)
        if not investigation:
            raise HTTPException(status_code=404, detail="Investigation not found")
        return investigation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get investigation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get investigation: {str(e)}")


@router.get("/stats/summary", response_model=OSINTStatsResponse)
async def get_statistics():
    """
    Get OSINT investigation statistics
    
    Returns summary statistics including:
    - Total investigations performed
    - Breakdown by investigation type
    - Breakdown by risk level
    - Average risk score
    - Total breaches found
    - Total social profiles found
    """
    try:
        stats = await osint_service.get_statistics()
        return OSINTStatsResponse(**stats)
    except Exception as e:
        logger.error(f"Failed to get statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")

# Made with Bob
