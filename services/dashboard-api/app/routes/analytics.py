from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter()

@router.get("/timeline")
async def get_timeline(hours: int = Query(24, ge=1, le=168), db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.get_timeline_chart(hours)

@router.get("/endpoints")
async def get_top_endpoints(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.get_endpoints_chart(limit)

@router.get("/sources")
async def get_top_sources(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.get_sources_chart(limit)

@router.get("/event-types")
async def get_event_types(db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.get_event_types_chart()
