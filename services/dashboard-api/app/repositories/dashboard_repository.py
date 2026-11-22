from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.database import ThreatEvent
from datetime import datetime, timezone, timedelta
from typing import List, Optional

class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_summary_metrics(self) -> dict:
        total_events = self.db.query(ThreatEvent).count()
        unique_attackers = self.db.query(func.count(func.distinct(ThreatEvent.source_ip))).scalar() or 0
        
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        events_today = self.db.query(ThreatEvent).filter(ThreatEvent.timestamp >= today_start).count()

        return {
            "total_events": total_events,
            "unique_attackers": unique_attackers,
            "events_today": events_today,
            "decoy_status": "ONLINE"
        }

    def list_events(
        self,
        limit: int = 50,
        offset: int = 0,
        event_type: Optional[str] = None,
        source_ip: Optional[str] = None,
        severity: Optional[str] = None
    ) -> List[ThreatEvent]:
        query = self.db.query(ThreatEvent)
        if event_type:
            query = query.filter(ThreatEvent.event_type == event_type)
        if source_ip:
            query = query.filter(ThreatEvent.source_ip == source_ip)
        if severity:
            query = query.filter(ThreatEvent.severity == severity)
        return query.order_by(desc(ThreatEvent.timestamp)).offset(offset).limit(limit).all()

    def get_event_by_id(self, event_id: str) -> Optional[ThreatEvent]:
        return self.db.query(ThreatEvent).filter(ThreatEvent.id == event_id).first()

    def get_top_endpoints(self, limit: int = 10):
        return (
            self.db.query(ThreatEvent.endpoint, func.count(ThreatEvent.id).label("count"))
            .group_by(ThreatEvent.endpoint)
            .order_by(desc("count"))
            .limit(limit)
            .all()
        )

    def get_top_sources(self, limit: int = 10):
        return (
            self.db.query(
                ThreatEvent.source_ip,
                func.count(ThreatEvent.id).label("count"),
                func.max(ThreatEvent.timestamp).label("last_seen")
            )
            .group_by(ThreatEvent.source_ip)
            .order_by(desc("count"))
            .limit(limit)
            .all()
        )

    def get_event_types_distribution(self):
        return (
            self.db.query(ThreatEvent.event_type, func.count(ThreatEvent.id).label("count"))
            .group_by(ThreatEvent.event_type)
            .order_by(desc("count"))
            .all()
        )

    def get_timeline(self, hours: int = 24):
        since = datetime.now(timezone.utc) - timedelta(hours=hours)
        records = (
            self.db.query(
                func.date_trunc('hour', ThreatEvent.timestamp).label("time_bucket"),
                func.count(ThreatEvent.id).label("count")
            )
            .filter(ThreatEvent.timestamp >= since)
            .group_by("time_bucket")
            .order_by("time_bucket")
            .all()
        )
        return records
