# Updated: Added Chat Assistant routes
"""
SentinelX AI - Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database.mongodb import connect_to_mongo, close_mongo_connection, create_indexes
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="SentinelX AI",
    description="AI-Powered Cyber Investigation & Threat Intelligence Assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("Starting SentinelX AI...")
    await connect_to_mongo()
    await create_indexes()
    logger.info("SentinelX AI started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Shutting down SentinelX AI...")
    await close_mongo_connection()
    logger.info("SentinelX AI shut down successfully")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SentinelX AI API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SentinelX AI",
        "version": "1.0.0"
    }


# Import and include routers
from app.routes import phishing, osint, threat, report, chat, dashboard

app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(phishing.router, prefix="/api/phishing", tags=["Phishing"])
app.include_router(osint.router, prefix="/api/osint", tags=["OSINT"])
app.include_router(threat.router, prefix="/api/threat", tags=["Threat Intelligence"])
app.include_router(report.router, prefix="/api/report", tags=["Incident Reports"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat Assistant"])

# Additional routers will be added as features are built
# from app.routes import threat_intel, reports, chat
# app.include_router(threat_intel.router, prefix="/api/threats", tags=["Threats"])
# app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
# app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )

# Made with Bob
