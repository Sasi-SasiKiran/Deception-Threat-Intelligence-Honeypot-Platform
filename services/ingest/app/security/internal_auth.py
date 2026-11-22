from app.config import settings
import secrets

def verify_internal_token(token: str) -> bool:
    """
    Constant-time comparison to prevent timing attacks on internal token verification.
    """
    if not token or not settings.internal_api_key:
        return False
    return secrets.compare_digest(token, settings.internal_api_key)
