"""
Dashboard API Routes
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import random

router = APIRouter()


@router.get("/overview")
async def get_dashboard_overview():
    """Get dashboard overview statistics"""
    try:
        # Mock data for now - replace with real database queries
        return {
            "stats": {
                "threats_detected": 1234,
                "threats_change": -12,
                "phishing_attempts": 567,
                "phishing_change": -8,
                "active_investigations": 89,
                "investigations_change": 15,
                "reports_generated": 342,
                "reports_change": 23
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/activity")
async def get_recent_activity():
    """Get recent activity feed"""
    try:
        # Mock data
        activities = [
            {
                "id": "1",
                "type": "threat",
                "severity": "critical",
                "title": "Critical Threat Detected",
                "description": "Suspicious activity from IP 192.168.1.100",
                "timestamp": (datetime.utcnow() - timedelta(minutes=5)).isoformat()
            },
            {
                "id": "2",
                "type": "phishing",
                "severity": "high",
                "title": "Phishing Email Blocked",
                "description": "Malicious email targeting finance department",
                "timestamp": (datetime.utcnow() - timedelta(minutes=15)).isoformat()
            },
            {
                "id": "3",
                "type": "investigation",
                "severity": "medium",
                "title": "OSINT Investigation Completed",
                "description": "Investigation for user@example.com finished",
                "timestamp": (datetime.utcnow() - timedelta(hours=1)).isoformat()
            },
            {
                "id": "4",
                "type": "report",
                "severity": "low",
                "title": "Incident Report Generated",
                "description": "Monthly security report created",
                "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat()
            }
        ]
        return {"activities": activities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends")
async def get_threat_trends():
    """Get threat trends for charts"""
    try:
        # Generate mock trend data for last 7 days
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        trends = {
            "labels": days,
            "datasets": [
                {
                    "label": "Malware",
                    "data": [random.randint(30, 60) for _ in days],
                    "color": "#ef4444"
                },
                {
                    "label": "Phishing",
                    "data": [random.randint(15, 30) for _ in days],
                    "color": "#f59e0b"
                },
                {
                    "label": "Total Threats",
                    "data": [random.randint(40, 70) for _ in days],
                    "color": "#dc2626"
                }
            ]
        }
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/distribution")
async def get_threat_distribution():
    """Get threat type distribution"""
    try:
        distribution = {
            "phishing": 567,
            "malware": 342,
            "ransomware": 156,
            "ddos": 89,
            "data_breach": 80
        }
        return distribution
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Made with Bob
