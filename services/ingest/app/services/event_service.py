from sqlalchemy.orm import Session
from app.repositories.event_repository import EventRepository
from app.validators.event_validator import validate_event_data
from app.validators.payload_validator import validate_payload_size
from app.normalizers.event_normalizer import normalize_threat_event
from app.schemas.event_schema import ThreatEventCreate
import logging

logger = logging.getLogger("ingest.service")

class EventService:
    def __init__(self, db: Session):
        self.repo = EventRepository(db)

    def process_and_store_event(self, event_create: ThreatEventCreate) -> dict:
        """
        Coordinates full ingest pipeline:
        1. Validates payload size
        2. Validates event attributes
        3. Normalizes fields
        4. Persists record in isolated PostgreSQL database
        """
        raw_dict = event_create.model_dump()
        
        # 1. Size constraint check
        validate_payload_size(raw_dict)
        
        # 2. Logic & IP validation
        validate_event_data(raw_dict)
        
        # 3. Data normalization
        clean_data = normalize_threat_event(raw_dict)
        
        # 4. Storage
        saved_record = self.repo.save_event(clean_data)
        logger.info(f"Ingested event id={saved_record.id} type={saved_record.event_type} from {saved_record.source_ip}")
        
        return {
            "id": str(saved_record.id),
            "timestamp": saved_record.timestamp,
            "source_ip": saved_record.source_ip,
            "method": saved_record.method,
            "endpoint": saved_record.endpoint,
            "event_type": saved_record.event_type,
            "status_code": saved_record.status_code,
            "severity": saved_record.severity
        }
