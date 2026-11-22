from app.config import settings

def get_internal_auth_headers() -> dict:
    """Returns the internal service-to-service authentication headers."""
    return {
        "X-Internal-Token": settings.internal_api_key,
        "Content-Type": "application/json"
    }
