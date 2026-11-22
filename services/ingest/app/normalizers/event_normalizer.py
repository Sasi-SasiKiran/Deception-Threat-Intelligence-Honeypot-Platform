from datetime import datetime, timezone

def normalize_threat_event(event_dict: dict) -> dict:
    """
    Standardizes timestamps to UTC ISO strings, trims strings,
    lowercases method and severity fields, and ensures passwords remain redacted.
    """
    normalized = event_dict.copy()

    # Normalize timestamp
    if not normalized.get("timestamp"):
        normalized["timestamp"] = datetime.now(timezone.utc)

    # Lowercase & trim
    normalized["method"] = normalized.get("method", "GET").upper().strip()
    normalized["endpoint"] = normalized.get("endpoint", "/").strip()
    normalized["severity"] = normalized.get("severity", "low").lower().strip()
    normalized["source_ip"] = normalized.get("source_ip", "").strip()

    # Redaction safety check on payload
    payload = normalized.get("payload_summary", {})
    if isinstance(payload, dict):
        for k in list(payload.keys()):
            if any(term in k.lower() for term in ["pass", "pwd", "token", "secret"]):
                payload[k] = "[REDACTED]"
    normalized["payload_summary"] = payload

    return normalized
