import os
from pydantic_settings import BaseSettings

class DashboardApiSettings(BaseSettings):
    app_name: str = "Threat Intelligence Dashboard API"
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Read-only or restricted database connection
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://honeypot_admin:honeypot_secure_pass_2026!@database:5432/threat_intelligence"
    )

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = DashboardApiSettings()
