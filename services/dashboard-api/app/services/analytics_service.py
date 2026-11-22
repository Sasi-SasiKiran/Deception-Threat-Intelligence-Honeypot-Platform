from sqlalchemy.orm import Session
from app.repositories.dashboard_repository import DashboardRepository

class AnalyticsService:
    def __init__(self, db: Session):
        self.repo = DashboardRepository(db)

    def get_timeline_chart(self, hours: int = 24):
        rows = self.repo.get_timeline(hours)
        return [
            {"time": r.time_bucket.isoformat() if r.time_bucket else "", "count": r.count}
            for r in rows
        ]

    def get_endpoints_chart(self, limit: int = 10):
        rows = self.repo.get_top_endpoints(limit)
        return [{"endpoint": r.endpoint, "count": r.count} for r in rows]

    def get_sources_chart(self, limit: int = 10):
        rows = self.repo.get_top_sources(limit)
        return [
            {
                "source_ip": r.source_ip,
                "count": r.count,
                "last_seen": r.last_seen.isoformat() if r.last_seen else ""
            }
            for r in rows
        ]

    def get_event_types_chart(self):
        rows = self.repo.get_event_types_distribution()
        return [{"event_type": r.event_type, "count": r.count} for r in rows]
