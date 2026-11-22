from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.database.connection import Base

class ThreatEvent(Base):
    __tablename__ = "threat_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    source_ip = Column(String(45), nullable=False, index=True)
    method = Column(String(10), nullable=False)
    endpoint = Column(String(512), nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True)
    user_agent = Column(String(512), nullable=True)
    payload_summary = Column(JSONB, default=dict)
    headers = Column(JSONB, default=dict)
    status_code = Column(Integer, nullable=False)
    severity = Column(String(20), default="low", nullable=False, index=True)
    fingerprint = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
