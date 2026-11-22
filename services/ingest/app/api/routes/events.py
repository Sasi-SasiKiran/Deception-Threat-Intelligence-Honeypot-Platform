from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.event_schema import ThreatEventCreate, ThreatEventResponse
from app.security.authentication import require_internal_auth
from app.services.event_service import EventService

router = APIRouter()

@router.post("/events", response_model=ThreatEventResponse, status_code=status.HTTP_201_CREATED)
async def submit_threat_event(
    event_data: ThreatEventCreate,
    db: Session = Depends(get_db),
    authorized: bool = Depends(require_internal_auth)
):
    """
    Authenticated internal endpoint to validate, normalize, and store threat events from decoys.
    """
    service = EventService(db)
    result = service.process_and_store_event(event_data)
    return result
