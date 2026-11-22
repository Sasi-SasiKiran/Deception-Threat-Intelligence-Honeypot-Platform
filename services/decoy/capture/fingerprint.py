import hashlib

def generate_request_fingerprint(source_ip: str, user_agent: str, method: str) -> str:
    """
    Computes a non-invasive SHA-256 fingerprint from client metadata.
    Avoids invasive device tracking or collecting unnecessary PII.
    """
    raw_str = f"{source_ip}|{user_agent}|{method}"
    return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()[:16]
