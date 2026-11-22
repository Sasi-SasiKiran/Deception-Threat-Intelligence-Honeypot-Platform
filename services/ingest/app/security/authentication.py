from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.security.internal_auth import verify_internal_token

API_KEY_HEADER = APIKeyHeader(name="X-Internal-Token", auto_error=False)

async def require_internal_auth(api_key: str = Security(API_KEY_HEADER)):
    """
    FastAPI dependency ensuring caller presents the valid internal service key.
    Rejects unauthorized external requests with HTTP 401.
    """
    if not api_key or not verify_internal_token(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized internal service access. Invalid or missing X-Internal-Token."
        )
    return True
