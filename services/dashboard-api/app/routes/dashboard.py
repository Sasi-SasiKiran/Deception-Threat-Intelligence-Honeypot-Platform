from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.dashboard_service import DashboardService

router = APIRouter()

@router.get("/summary")
async def get_dashboard_summary(db: Session = Depends(get_db)):
    service = DashboardService(db)
    return service.get_overview()
