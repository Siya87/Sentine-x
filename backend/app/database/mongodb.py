"""
MongoDB database connection and management
"""
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class Database:
    """Database connection manager"""
    client: AsyncIOMotorClient = None
    db = None


db = Database()


async def connect_to_mongo():
    """Connect to MongoDB"""
    logger.info("Connecting to MongoDB...")
    try:
        # Configure MongoDB client with relaxed SSL settings for Railway deployment
        db.client = AsyncIOMotorClient(
            settings.mongodb_uri,
            tls=True,
            tlsAllowInvalidCertificates=True,  # Relaxed for Railway
            serverSelectionTimeoutMS=30000,    # Increased to 30 seconds
            connectTimeoutMS=30000,            # Increased to 30 seconds
            socketTimeoutMS=30000,             # Increased to 30 seconds
            retryWrites=True,
            w='majority'
        )
        db.db = db.client.sentinelx
        # Test connection
        await db.client.admin.command('ping')
        logger.info("✅ Successfully connected to MongoDB")
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        logger.error(f"Connection URI (masked): {settings.mongodb_uri[:30]}...")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    logger.info("Closing MongoDB connection...")
    if db.client:
        db.client.close()
        logger.info("MongoDB connection closed")


def get_database():
    """Get database instance"""
    return db.db


async def create_indexes():
    """Create database indexes for better performance"""
    logger.info("Creating database indexes...")
    
    # Phishing analyses indexes
    await db.db.phishing_analyses.create_index("analysis_id", unique=True)
    await db.db.phishing_analyses.create_index([("created_at", -1)])
    await db.db.phishing_analyses.create_index([("ai_analysis.threat_score", -1)])
    
    # OSINT investigations indexes
    await db.db.osint_investigations.create_index("investigation_id", unique=True)
    await db.db.osint_investigations.create_index("target")
    await db.db.osint_investigations.create_index([("created_at", -1)])
    
    # Threat intelligence indexes
    await db.db.threat_intelligence.create_index("threat_id", unique=True)
    await db.db.threat_intelligence.create_index([("timestamp", -1)])
    await db.db.threat_intelligence.create_index([("threat_type", 1), ("severity", 1)])
    await db.db.threat_intelligence.create_index([("location", "2dsphere")])
    
    # Incident reports indexes
    await db.db.incident_reports.create_index("report_id", unique=True)
    await db.db.incident_reports.create_index("incident_id")
    await db.db.incident_reports.create_index([("created_at", -1)])
    
    # Chat sessions indexes
    await db.db.chat_sessions.create_index("session_id", unique=True)
    await db.db.chat_sessions.create_index([("last_activity", -1)])
    await db.db.chat_sessions.create_index([("created_at", -1)])
    
    logger.info("Database indexes created successfully")

# Made with Bob
