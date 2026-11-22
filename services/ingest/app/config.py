import os
from pydantic_settings import BaseSettings

class IngestSettings(BaseSettings):
    app_name: str = "Internal Ingest API"
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Internal service auth token
    internal_api_key: str = os.getenv("INTERNAL_API_KEY", "sec_honeypot_internal_token_9f82d17c91a04b")
    
    # PostgreSQL Connection String
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://honeypot_admin:honeypot_secure_pass_2026!@database:5432/threat_intelligence"
    )
    
    # Maximum payload size in bytes
    max_payload_size: int = 65536

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = IngestSettings()
