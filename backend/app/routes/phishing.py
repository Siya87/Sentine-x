"""
Phishing Detection API Routes
"""
from fastapi import APIRouter, HTTPException, Query
from app.models.phishing import (
    PhishingAnalysisRequest,
    PhishingAnalysisResponse,
    PhishingAnalysisListResponse
)
from app.services.phishing_service import PhishingService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
service = PhishingService()


@router.post("/analyze", response_model=PhishingAnalysisResponse, status_code=200)
async def analyze_phishing(request: PhishingAnalysisRequest):
    """
    Analyze content for phishing indicators
    
    - **content_type**: Type of content (email, url, sms, file)
    - **content**: The content to analyze
    - **sender**: Optional sender information
    - **metadata**: Optional additional metadata
    
    Returns detailed analysis with threat score, indicators, and recommendations.
    """
    try:
        logger.info(f"Received phishing analysis request: {request.content_type}")
        result = await service.analyze(request.dict())
        return result
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")


@router.get("/history", response_model=PhishingAnalysisListResponse)
async def get_history(
    limit: int = Query(10, ge=1, le=100, description="Number of results to return"),
    skip: int = Query(0, ge=0, description="Number of results to skip")
):
    """
    Get phishing analysis history
    
    - **limit**: Number of results to return (1-100)
    - **skip**: Number of results to skip for pagination
    
    Returns list of previous analyses.
    """
    try:
        result = await service.get_history(limit=limit, skip=skip)
        return result
    except Exception as e:
        logger.error(f"Failed to get history: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve history")


@router.get("/{analysis_id}")
async def get_analysis(analysis_id: str):
    """
    Get specific analysis by ID
    
    - **analysis_id**: Unique analysis identifier
    
    Returns detailed analysis information.
    """
    try:
        result = await service.get_analysis(analysis_id)
        return result
    except ValueError as e:
        logger.error(f"Analysis not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve analysis")


@router.get("/stats/summary")
async def get_statistics():
    """
    Get phishing analysis statistics
    
    Returns summary statistics including:
    - Total analyses performed
    - Number of phishing attempts detected
    - Average threat score
    - Breakdown by content type
    """
    try:
        result = await service.get_statistics()
        return result
    except Exception as e:
        logger.error(f"Failed to get statistics: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")

# Made with Bob
