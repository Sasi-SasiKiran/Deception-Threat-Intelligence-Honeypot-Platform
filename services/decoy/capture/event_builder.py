from datetime import datetime, timezone
from typing import Dict, Any
from app.capture.fingerprint import generate_request_fingerprint

def build_threat_event(
    metadata: Dict[str, Any],
    event_type: str,
    status_code: int,
    severity: str,
    payload_summary: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Constructs a standardized Threat Event payload ready for internal ingestion.
    """
    source_ip = metadata.get("source_ip", "127.0.0.1")
    user_agent = metadata.get("user_agent", "Unknown")
    method = metadata.get("method", "GET")
    endpoint = metadata.get("endpoint", "/")

    fingerprint = generate_request_fingerprint(source_ip, user_agent, method)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_ip": source_ip,
        "method": method,
        "endpoint": endpoint,
        "event_type": event_type,
        "user_agent": user_agent,
        "payload_summary": payload_summary or {},
        "headers": metadata.get("headers", {}),
        "status_code": status_code,
        "severity": severity,
        "fingerprint": fingerprint
    }
