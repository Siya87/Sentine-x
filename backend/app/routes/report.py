# Updated: Fixed statistics endpoint limit validation
"""
Incident Report API Routes
Endpoints for AI-powered incident report generation and management
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
import logging

from app.models.report import (
    IncidentReport, ReportGenerationRequest, ReportSearchRequest,
    ReportListResponse, ReportUpdateRequest, PDFExportRequest
)
from app.services.report_service import ReportService

logger = logging.getLogger(__name__)

router = APIRouter()
report_service = ReportService()


@router.post("/generate", response_model=IncidentReport, status_code=status.HTTP_201_CREATED)
async def generate_report(request: ReportGenerationRequest):
    """
    Generate a comprehensive incident report using AI
    
    This endpoint uses IBM Granite AI to automatically generate:
    - Executive summary
    - Technical analysis
    - Attack vectors with MITRE ATT&CK mapping
    - Timeline of events
    - Mitigation steps
    - Recommendations
    
    The generated report is stored in the database and can be exported to PDF.
    """
    try:
        logger.info(f"Generating incident report: {request.title}")
        report = await report_service.generate_report(request)
        return report
    except Exception as e:
        logger.error(f"Failed to generate report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate report: {str(e)}"
        )


@router.get("/{report_id}", response_model=IncidentReport)
async def get_report(report_id: str):
    """
    Get a specific incident report by ID
    
    Retrieves the complete incident report including all sections,
    timeline, mitigation steps, and recommendations.
    """
    try:
        logger.info(f"Retrieving report: {report_id}")
        report = await report_service.get_report(report_id)
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report {report_id} not found"
            )
        
        return report
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve report {report_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve report: {str(e)}"
        )


@router.post("/search", response_model=ReportListResponse)
async def search_reports(request: ReportSearchRequest):
    """
    Search incident reports with filters
    
    Search and filter reports by:
    - Incident type
    - Severity level
    - Status
    - Date range
    - Text search in title and summary
    
    Results are paginated and sorted by creation date (newest first).
    """
    try:
        logger.info(f"Searching reports with filters: {request.model_dump()}")
        results = await report_service.search_reports(request)
        return results
    except Exception as e:
        logger.error(f"Failed to search reports: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search reports: {str(e)}"
        )


@router.get("/list/all", response_model=ReportListResponse)
async def list_all_reports(limit: int = 10, skip: int = 0):
    """
    List all incident reports
    
    Returns a paginated list of all incident reports,
    sorted by creation date (newest first).
    """
    try:
        logger.info(f"Listing all reports (limit={limit}, skip={skip})")
        request = ReportSearchRequest(
            incident_type=None,
            severity=None,
            status=None,
            start_date=None,
            end_date=None,
            search_text=None,
            limit=limit,
            skip=skip
        )
        results = await report_service.search_reports(request)
        return results
    except Exception as e:
        logger.error(f"Failed to list reports: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list reports: {str(e)}"
        )


@router.patch("/{report_id}", response_model=IncidentReport)
async def update_report(report_id: str, update: ReportUpdateRequest):
    """
    Update an existing incident report
    
    Allows updating:
    - Incident status
    - Additional notes
    - Mitigation steps
    - Recommendations
    
    The updated_at timestamp is automatically updated.
    """
    try:
        logger.info(f"Updating report: {report_id}")
        report = await report_service.update_report(report_id, update)
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report {report_id} not found"
            )
        
        return report
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update report {report_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update report: {str(e)}"
        )


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(report_id: str):
    """
    Delete an incident report
    
    Permanently deletes the specified incident report from the database.
    This action cannot be undone.
    """
    try:
        logger.info(f"Deleting report: {report_id}")
        success = await report_service.delete_report(report_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report {report_id} not found"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete report {report_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete report: {str(e)}"
        )


@router.post("/{report_id}/export/pdf")
async def export_report_pdf(report_id: str, request: PDFExportRequest):
    """
    Export incident report as PDF
    
    Generates a professionally formatted PDF document of the incident report.
    The PDF includes all report sections, charts, and can optionally include attachments.
    
    Note: PDF generation functionality is currently in development.
    This endpoint returns a placeholder response.
    """
    try:
        logger.info(f"Exporting report {report_id} to PDF")
        
        # Get the report
        report = await report_service.get_report(report_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report {report_id} not found"
            )
        
        # TODO: Implement PDF generation
        # For now, return a placeholder response
        return {
            "message": "PDF export functionality coming soon",
            "report_id": report_id,
            "template": request.template,
            "status": "pending"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to export report {report_id} to PDF: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export report: {str(e)}"
        )


@router.get("/stats/summary")
async def get_report_statistics():
    """
    Get incident report statistics
    
    Returns summary statistics about incident reports:
    - Total number of reports
    - Reports by severity
    - Reports by type
    - Reports by status
    - Recent activity
    """
    try:
        logger.info("Fetching report statistics")
        
        # Get all reports for statistics
        all_reports = await report_service.search_reports(
            ReportSearchRequest(
                incident_type=None,
                severity=None,
                status=None,
                start_date=None,
                end_date=None,
                search_text=None,
                limit=100,
                skip=0
            )
        )
        
        # Calculate statistics
        stats = {
            "total_reports": all_reports.total,
            "by_severity": {},
            "by_type": {},
            "by_status": {},
            "recent_count": 0
        }
        
        # Count by categories
        for report in all_reports.reports:
            # By severity
            severity = report.severity.value
            stats["by_severity"][severity] = stats["by_severity"].get(severity, 0) + 1
            
            # By type
            incident_type = report.incident_type.value
            stats["by_type"][incident_type] = stats["by_type"].get(incident_type, 0) + 1
            
            # By status
            status_val = report.status.value
            stats["by_status"][status_val] = stats["by_status"].get(status_val, 0) + 1
        
        # Recent reports (last 10)
        stats["recent_count"] = min(10, all_reports.total)
        
        return stats
    except Exception as e:
        logger.error(f"Failed to get report statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get statistics: {str(e)}"
        )

# Made with Bob
