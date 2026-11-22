from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings
import uuid

engine = create_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ThreatEvent(Base):
    __tablename__ = "threat_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    source_ip = Column(String(45), nullable=False)
    method = Column(String(10), nullable=False)
    endpoint = Column(String(512), nullable=False)
    event_type = Column(String(50), nullable=False)
    user_agent = Column(String(512), nullable=True)
    payload_summary = Column(JSONB, default=dict)
    headers = Column(JSONB, default=dict)
    status_code = Column(Integer, nullable=False)
    severity = Column(String(20), default="low", nullable=False)
    fingerprint = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
