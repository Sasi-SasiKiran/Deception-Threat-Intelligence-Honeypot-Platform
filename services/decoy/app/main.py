from fastapi import FastAPI
import logging
from app.config import settings
from app.routes import login, pages, probes

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger("decoy.main")

app = FastAPI(
    title=settings.app_name,
    description="WordPress Emulation Honeypot Decoy Service",
    version="1.0.0"
)

# Register routes
app.include_router(pages.router, tags=["Pages"])
app.include_router(login.router, tags=["Authentication Decoy"])
app.include_router(probes.router, tags=["Probes & Honeytraps"])

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "decoy"}
