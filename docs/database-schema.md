# Database Schema Specification

## Database: `threat_intelligence`
Engine: PostgreSQL 15+

### Table: `threat_events`
Stores normalized security events captured by the honeypot decoys.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier for event |
| `timestamp` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Time the event was captured |
| `source_ip` | VARCHAR(45) | NOT NULL | IPv4 or IPv6 address of the client |
| `method` | VARCHAR(10) | NOT NULL | HTTP Method (GET, POST, HEAD, etc.) |
| `endpoint` | VARCHAR(512) | NOT NULL | Requested URI path |
| `event_type` | VARCHAR(50) | NOT NULL | Classification (`login_attempt`, `path_probe`, etc.) |
| `user_agent` | VARCHAR(512) | NULL | Client HTTP User-Agent string |
| `payload_summary`| JSONB | NULL, DEFAULT '{}' | Sanitized payload metadata (passwords redacted) |
| `headers` | JSONB | NULL, DEFAULT '{}' | Captured HTTP headers |
| `status_code` | INTEGER | NOT NULL | HTTP status code returned to attacker (e.g. 401) |
| `severity` | VARCHAR(20) | NOT NULL, DEFAULT 'low' | Severity level (`low`, `medium`, `high`, `critical`) |
| `fingerprint` | VARCHAR(64) | NULL | SHA-256 hash computed from IP + UA + header characteristics |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Record creation timestamp |

### Indexes
- `idx_threat_events_timestamp`: B-TREE on `timestamp DESC` (optimizes timeline queries)
- `idx_threat_events_source_ip`: B-TREE on `source_ip` (optimizes attacker profile queries)
- `idx_threat_events_event_type`: B-TREE on `event_type`
- `idx_threat_events_endpoint`: B-TREE on `endpoint`
- `idx_threat_events_severity`: B-TREE on `severity`
