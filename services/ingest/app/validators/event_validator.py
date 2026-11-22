import ipaddress
from fastapi import HTTPException

ALLOWED_EVENT_TYPES = {
    "login_attempt",
    "path_probe",
    "page_access",
    "invalid_request",
    "suspicious_request"
}

ALLOWED_SEVERITIES = {"low", "medium", "high", "critical"}

def validate_event_data(event_dict: dict) -> bool:
    """
    Validates IP format, event classification, and severity bounds.
    """
    # IP validation
    source_ip = event_dict.get("source_ip", "")
    try:
        ipaddress.ip_address(source_ip)
    except ValueError:
        raise HTTPException(status_code=422, detail=f"Invalid IP address format: {source_ip}")

    # Event Type validation
    event_type = event_dict.get("event_type", "")
    if event_type not in ALLOWED_EVENT_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown event_type '{event_type}'. Allowed types: {list(ALLOWED_EVENT_TYPES)}"
        )

    # Severity validation
    severity = event_dict.get("severity", "low").lower()
    if severity not in ALLOWED_SEVERITIES:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid severity '{severity}'. Allowed values: {list(ALLOWED_SEVERITIES)}"
        )

    return True
