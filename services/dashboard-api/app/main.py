from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import dashboard, events, analytics, health
import logging

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger("dashboard_api.main")

app = FastAPI(
    title=settings.app_name,
    description="Read-Only Telemetry & Threat Intelligence Dashboard API",
    version="1.0.0"
)

# Enable CORS for React frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard Summary"])
app.include_router(events.router, prefix="/api/events", tags=["Event Feeds"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics & Visualizations"])
app.include_router(health.router, prefix="/api", tags=["Health"])

@app.get("/")
async def root():
    return {"message": "Threat Intelligence Dashboard API is active", "version": "1.0.0"}
