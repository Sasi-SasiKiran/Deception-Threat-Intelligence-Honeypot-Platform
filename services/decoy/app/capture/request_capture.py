from fastapi import Request
from typing import Dict, Any

async def extract_request_metadata(request: Request) -> Dict[str, Any]:
    """
    Extracts permitted, safe request metadata including real source IP, headers, and query params.
    """
    # Prefer trusted reverse-proxy header X-Real-IP if configured, fallback to client.host
    client_ip = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For")
    if client_ip:
        client_ip = client_ip.split(",")[0].strip()
    else:
        client_ip = request.client.host if request.client else "127.0.0.1"

    user_agent = request.headers.get("user-agent", "Unknown")[:512]
    
    # Extract headers (filtering out oversized cookies)
    headers_dict = {}
    for k, v in request.headers.items():
        if k.lower() not in ["cookie", "authorization"]:
            headers_dict[k] = v[:256]

    return {
        "source_ip": client_ip,
        "method": request.method,
        "endpoint": request.url.path,
        "query_params": str(request.query_params),
        "user_agent": user_agent,
        "headers": headers_dict
    }

def sanitize_payload(payload: Any) -> Dict[str, Any]:
    """
    Strictly sanitizes user submitted payloads. Never stores submitted passwords in plaintext!
    """
    if not isinstance(payload, dict):
        return {"raw_summary": str(payload)[:256]}

    sanitized = {}
    for key, val in payload.items():
        lower_k = key.lower()
        if any(secret_term in lower_k for secret_term in ["password", "pwd", "secret", "token", "auth"]):
            sanitized[key] = "[REDACTED]"
        else:
            sanitized[key] = str(val)[:256]
            
    return sanitized
