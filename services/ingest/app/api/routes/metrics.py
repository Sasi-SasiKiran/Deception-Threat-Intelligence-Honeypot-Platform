from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.security.authentication import require_internal_auth
from app.services.metrics_service import MetricsService

router = APIRouter()

@router.get("/metrics")
async def ingest_metrics(
    db: Session = Depends(get_db),
    authorized: bool = Depends(require_internal_auth)
):
    service = MetricsService(db)
    return service.get_ingest_metrics()
