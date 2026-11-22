from fastapi import HTTPException
from app.config import settings
import json

def validate_payload_size(payload: dict) -> bool:
    """
    Prevents oversized payload injection or log memory exhaustion attacks.
    """
    try:
        raw_size = len(json.dumps(payload, default=str))
        if raw_size > settings.max_payload_size:
            raise HTTPException(
                status_code=413,
                detail=f"Payload size {raw_size} bytes exceeds allowed limit of {settings.max_payload_size} bytes."
            )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail=f"Invalid JSON structure: {e}")
    return True
