from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.dashboard_service import DashboardService
from typing import Optional

router = APIRouter()

@router.get("")
async def list_events(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    event_type: Optional[str] = None,
    source_ip: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = DashboardService(db)
    return service.get_events(limit, offset, event_type, source_ip, severity)

@router.get("/{event_id}")
async def get_event_detail(event_id: str, db: Session = Depends(get_db)):
    service = DashboardService(db)
    detail = service.get_event_detail(event_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Event not found")
    return detail
