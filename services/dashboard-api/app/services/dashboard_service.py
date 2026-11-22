from sqlalchemy.orm import Session
from app.repositories.dashboard_repository import DashboardRepository

class DashboardService:
    def __init__(self, db: Session):
        self.repo = DashboardRepository(db)

    def get_overview(self) -> dict:
        return self.repo.get_summary_metrics()

    def get_events(self, limit: int = 50, offset: int = 0, event_type: str = None, source_ip: str = None, severity: str = None):
        records = self.repo.list_events(limit, offset, event_type, source_ip, severity)
        return [
            {
                "id": str(r.id),
                "timestamp": r.timestamp,
                "source_ip": r.source_ip,
                "method": r.method,
                "endpoint": r.endpoint,
                "event_type": r.event_type,
                "user_agent": r.user_agent,
                "payload_summary": r.payload_summary,
                "status_code": r.status_code,
                "severity": r.severity,
                "fingerprint": r.fingerprint
            }
            for r in records
        ]

    def get_event_detail(self, event_id: str):
        record = self.repo.get_event_by_id(event_id)
        if not record:
            return None
        return {
            "id": str(record.id),
            "timestamp": record.timestamp,
            "source_ip": record.source_ip,
            "method": record.method,
            "endpoint": record.endpoint,
            "event_type": record.event_type,
            "user_agent": record.user_agent,
            "payload_summary": record.payload_summary,
            "headers": record.headers,
            "status_code": record.status_code,
            "severity": record.severity,
            "fingerprint": record.fingerprint,
            "created_at": record.created_at
        }
