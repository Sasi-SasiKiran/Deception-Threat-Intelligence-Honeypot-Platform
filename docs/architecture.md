# System Architecture

## Overview
The **Deception & Threat Intelligence Honeypot Platform** is an enterprise-grade deception framework engineered to attract, deflect, profile, and record malicious actors attempting web reconnaissance and unauthorized credential stuffing.

## Security Architecture Principles

### 1. Zero Trust & Network Segmentation
- **Attacker-Facing Zone**: The Nginx reverse proxy and the FastAPI Decoy are attached to an external-facing bridge network (`attacker-facing`).
- **Air-Gapped / Isolated Zone**: The PostgreSQL database and Ingest API reside in a segregated private Docker bridge (`internal-net`).
- **No Direct Decoy-to-Database Connection**: The decoy has no database drivers or credentials. If compromised, attackers cannot read or overwrite threat intelligence records.

### 2. One-Way Telemetry Pipeline
```
Attacker Request -> Nginx (Client IP extraction) -> Decoy Service (WordPress trap)
                 -> Authenticated Internal Ingest API (Token check + Payload normalizer)
                 -> Isolated PostgreSQL Storage
                 -> Dashboard API (Read-only aggregation)
                 -> SOC Frontend (Real-time monitoring)
```

## Component Roles
1. **Nginx Reverse Proxy**:
   Terminates public connections, preserves client source IP via `X-Real-IP`, rate-limits abusive volumetric floods, and proxies HTTP traffic to the Decoy.
2. **FastAPI Decoy**:
   Emulates a vulnerable WordPress 6.x instance. Exposes traps including `/wp-login.php`, `/wp-admin/`, `/xmlrpc.php`, `/robots.txt`, and hidden `.env` / `.git` probes. Returns realistic HTTP 401 Unauthorized responses without executing malicious payloads.
3. **Internal Ingest API**:
   Verifies service-to-service authentication using `X-Internal-Token`, validates schema compliance with Pydantic, applies strict sanitization (redacting passwords), normalizes event fields, and writes to PostgreSQL.
4. **PostgreSQL Database**:
   Persists threat records, client fingerprints, request metadata, and telemetry.
5. **Dashboard API**:
   Provides high-performance read-only analytics, top attacking IP aggregates, probe frequencies, and real-time event timelines.
6. **Dashboard UI**:
   A React + Vite single-page application displaying real-time metrics, interactive threat feeds, and attack categorization.
