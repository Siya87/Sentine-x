"""
Configuration management for SentinelX AI
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    virustotal_api_key: str = ""
    abuseipdb_api_key: str = ""
    haveibeenpwned_api_key: str = ""
    shodan_api_key: str = ""
    
    # IBM Cloud
    ibm_cloud_api_key: str = ""
    ibm_project_id: str = ""
    ibm_watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    
    # Database
    mongodb_uri: str = "mongodb://localhost:27017/sentinelx"
    
    # App Config
    debug: bool = False
    log_level: str = "INFO"
    environment: str = "development"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS origins string to list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Made with Bob
