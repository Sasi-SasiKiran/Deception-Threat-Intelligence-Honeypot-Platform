from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ThreatEventCreate(BaseModel):
    timestamp: Optional[datetime] = None
    source_ip: str = Field(..., max_length=45)
    method: str = Field(..., max_length=10)
    endpoint: str = Field(..., max_length=512)
    event_type: str = Field(..., max_length=50)
    user_agent: Optional[str] = Field(default="Unknown", max_length=512)
    payload_summary: Optional[Dict[str, Any]] = Field(default_factory=dict)
    headers: Optional[Dict[str, Any]] = Field(default_factory=dict)
    status_code: int = Field(..., ge=100, le=599)
    severity: str = Field(default="low", max_length=20)
    fingerprint: Optional[str] = Field(default=None, max_length=64)

class ThreatEventResponse(BaseModel):
    id: str
    timestamp: datetime
    source_ip: str
    method: str
    endpoint: str
    event_type: str
    status_code: int
    severity: str

    class Config:
        from_attributes = True
