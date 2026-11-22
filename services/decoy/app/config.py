import os
from pydantic_settings import BaseSettings

class DecoySettings(BaseSettings):
    app_name: str = "Decoy Honeypot Web Service"
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Internal Ingest Endpoint
    ingest_service_url: str = os.getenv("INGEST_SERVICE_URL", "http://ingest:8001/api/v1/events")
    internal_api_key: str = os.getenv("INTERNAL_API_KEY", "sec_honeypot_internal_token_9f82d17c91a04b")
    
    # Request capture limits
    max_payload_length: int = 4096
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = DecoySettings()
