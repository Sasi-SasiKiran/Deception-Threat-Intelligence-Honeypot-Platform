# API Documentation

## 1. Internal Ingest API (Port 8001)

### Authentication
Internal calls must supply the header:
```
X-Internal-Token: <INTERNAL_API_KEY>
```

### Endpoints

#### POST `/api/v1/events`
Submit an event captured by the honeypot decoy.

**Request Headers:**
- `Content-Type: application/json`
- `X-Internal-Token: <INTERNAL_API_KEY>`

**Request Body Example:**
```json
{
  "source_ip": "192.168.1.105",
  "method": "POST",
  "endpoint": "/wp-login.php",
  "event_type": "login_attempt",
  "user_agent": "Mozilla/5.0 (Hydra/v9.3)",
  "payload_summary": {
    "username": "admin",
    "password": "[REDACTED]"
  },
  "status_code": 401,
  "severity": "medium",
  "headers": {
    "Host": "localhost",
    "Accept": "*/*"
  }
}
```

**Responses:**
- `201 Created`: Event validated, normalized, and stored.
- `401 Unauthorized`: Missing or invalid internal token.
- `422 Unprocessable Entity`: Schema validation error.

#### GET `/api/v1/health`
Health check endpoint.
- `200 OK`: `{"status": "healthy", "service": "ingest"}`

#### GET `/api/v1/metrics`
Internal ingestion counters.
- `200 OK`: `{"total_ingested": 142, "status": "active"}`

---

## 2. Dashboard API (Port 8002)

### Endpoints

#### GET `/api/dashboard/summary`
Returns high-level KPI metrics for the dashboard header cards.
**Response (200 OK):**
```json
{
  "total_events": 150,
  "unique_attackers": 12,
  "events_today": 45,
  "decoy_status": "ONLINE"
}
```

#### GET `/api/events`
Query captured threat events with pagination and filtering.
**Query Parameters:**
- `limit` (default: 50, max: 200)
- `offset` (default: 0)
- `event_type` (optional string)
- `source_ip` (optional string)
- `severity` (optional string: low, medium, high, critical)

#### GET `/api/events/{id}`
Returns details of a specific event record.

#### GET `/api/analytics/timeline`
Returns aggregated event volume bucketed over time (hours/days).

#### GET `/api/analytics/endpoints`
Returns top targeted endpoints (e.g. `/wp-login.php`, `/admin`, `/robots.txt`).

#### GET `/api/analytics/sources`
Returns top attacker source IPs with request counts and first/last seen timestamps.

#### GET `/api/analytics/event-types`
Distribution of events grouped by classification (`login_attempt`, `path_probe`, etc.).

#### GET `/api/health`
Dashboard API health status.
