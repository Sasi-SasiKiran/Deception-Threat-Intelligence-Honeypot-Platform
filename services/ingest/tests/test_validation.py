import pytest
from app.validators.event_validator import validate_event_data
from app.validators.payload_validator import validate_payload_size
from app.normalizers.event_normalizer import normalize_threat_event
from fastapi import HTTPException

def test_validate_event_data_valid():
    valid_event = {
        "source_ip": "192.168.1.50",
        "event_type": "login_attempt",
        "severity": "high"
    }
    assert validate_event_data(valid_event) is True

def test_validate_event_data_invalid_ip():
    invalid_event = {
        "source_ip": "not_an_ip_address",
        "event_type": "login_attempt",
        "severity": "high"
    }
    with pytest.raises(HTTPException):
        validate_event_data(invalid_event)

def test_validate_event_data_invalid_type():
    invalid_event = {
        "source_ip": "10.0.0.1",
        "event_type": "malicious_unregistered_event_type",
        "severity": "high"
    }
    with pytest.raises(HTTPException):
        validate_event_data(invalid_event)

def test_normalize_threat_event_sanitizes_passwords():
    raw_event = {
        "source_ip": "10.0.0.2",
        "method": "post",
        "endpoint": "/wp-login.php",
        "severity": "HIGH",
        "payload_summary": {
            "username": "root",
            "password": "ClearTextPasswordShouldBeRedacted!",
            "admin_token": "secret_abc"
        }
    }
    cleaned = normalize_threat_event(raw_event)
    assert cleaned["method"] == "POST"
    assert cleaned["severity"] == "high"
    assert cleaned["payload_summary"]["password"] == "[REDACTED]"
    assert cleaned["payload_summary"]["admin_token"] == "[REDACTED]"
    assert cleaned["payload_summary"]["username"] == "root"
