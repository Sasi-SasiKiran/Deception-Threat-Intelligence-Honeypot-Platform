# Testing Guide

This guide covers synthetic testing, unit test suites, integration tests, and verification of network isolation.

## 1. Automated Unit & Integration Tests

Ensure dependencies are installed:
```bash
pip install pytest requests fastapi httpx
```

Run test suite:
```bash
# Run all tests
pytest tests/ -v

# Run integration tests specifically
pytest tests/integration/test_event_pipeline.py -v
pytest tests/integration/test_service_health.py -v
```

## 2. Controlled Manual Probing

Simulate typical attacker actions against the honeypot:

### A. WordPress Fake Login Attack
```bash
curl -i -X POST http://localhost/wp-login.php \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "log=admin&pwd=SuperSecretPassword123"
```
**Expected Response:** `401 Unauthorized` with realistic WordPress error html or JSON.

### B. Directory Traversal / Reconnaissance Probe
```bash
curl -i http://localhost/wp-admin/
curl -i http://localhost/robots.txt
curl -i http://localhost/.env
```
**Expected Response:** Decoy captures request as `path_probe` or `suspicious_request` and returns 404 or 403.

### C. Automated Synthetic Event Generator
Run the built-in generator to stream realistic events into the pipeline:
```powershell
python scripts/generate_demo_events.py --count 10 --delay 0.5
```

## 3. Network Isolation Verification

Verify that the isolated database cannot be reached directly from outside the internal network:
```powershell
# Attempt to connect to PostgreSQL port 5432 directly from host
Test-NetConnection -ComputerName localhost -Port 5432
```
In default production compose mode, the database service has no host port binding, confirming air-gapped isolation.
