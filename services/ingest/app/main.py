from fastapi import FastAPI
from app.config import settings
from app.api.routes import events, health, metrics
import logging

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger("ingest.main")

app = FastAPI(
    title=settings.app_name,
    description="Internal Threat Event Ingestion, Validation & Storage API",
    version="1.0.0"
)

# Register internal API routes
app.include_router(events.router, prefix="/api/v1", tags=["Events Ingest"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(metrics.router, prefix="/api/v1", tags=["Internal Metrics"])

@app.get("/")
async def root():
    return {"message": "Deception Platform Internal Ingest Service", "status": "online"}
