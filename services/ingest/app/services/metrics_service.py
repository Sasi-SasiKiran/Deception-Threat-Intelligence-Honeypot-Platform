from sqlalchemy.orm import Session
from app.repositories.event_repository import EventRepository

class MetricsService:
    def __init__(self, db: Session):
        self.repo = EventRepository(db)

    def get_ingest_metrics(self) -> dict:
        total = self.repo.count_total_events()
        return {
            "total_ingested_events": total,
            "status": "operational",
            "queue_depth": 0
        }
