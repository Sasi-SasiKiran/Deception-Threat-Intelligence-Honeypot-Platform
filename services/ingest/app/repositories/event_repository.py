from sqlalchemy.orm import Session
from app.database.models import ThreatEvent
import logging

logger = logging.getLogger("ingest.repository")

class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_event(self, event_data: dict) -> ThreatEvent:
        """Persists a normalized threat event into the PostgreSQL database."""
        event_obj = ThreatEvent(
            timestamp=event_data.get("timestamp"),
            source_ip=event_data.get("source_ip"),
            method=event_data.get("method"),
            endpoint=event_data.get("endpoint"),
            event_type=event_data.get("event_type"),
            user_agent=event_data.get("user_agent"),
            payload_summary=event_data.get("payload_summary", {}),
            headers=event_data.get("headers", {}),
            status_code=event_data.get("status_code"),
            severity=event_data.get("severity", "low"),
            fingerprint=event_data.get("fingerprint")
        )
        self.db.add(event_obj)
        self.db.commit()
        self.db.refresh(event_obj)
        return event_obj

    def count_total_events(self) -> int:
        """Returns total count of events stored."""
        return self.db.query(ThreatEvent).count()
