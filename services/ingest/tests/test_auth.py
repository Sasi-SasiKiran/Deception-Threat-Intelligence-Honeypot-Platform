from app.security.internal_auth import verify_internal_token
from app.config import settings

def test_verify_internal_token_success():
    valid_token = settings.internal_api_key
    assert verify_internal_token(valid_token) is True

def test_verify_internal_token_failure():
    invalid_token = "tampered_fake_key_9999"
    assert verify_internal_token(invalid_token) is False
    assert verify_internal_token("") is False
    assert verify_internal_token(None) is False
