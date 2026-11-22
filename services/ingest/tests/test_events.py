from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.database.connection import get_db
from app.config import settings

def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_events_unauthorized_without_token():
    client = TestClient(app)
    payload = {
        "source_ip": "192.168.1.100",
        "method": "POST",
        "endpoint": "/wp-login.php",
        "event_type": "login_attempt",
        "status_code": 401,
        "severity": "high"
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == 401
