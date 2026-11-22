# Deception & Threat Intelligence Honeypot Platform

A network-segmented, production-grade deception and threat intelligence platform designed to safely lure, delay, and fingerprint attackers while capturing actionable cyber threat intelligence into an isolated storage tier and providing real-time visibility through a modern SOC dashboard.


---

## 🏛️ System Architecture & Data Flow

The platform implements a strict **one-directional event pipeline** with dual-network isolation:

```
[Attacker / Internet Prober]
             │
             ▼  (Port 80 / HTTP)
┌──────────────────────────────────────────────┐
│            Nginx Reverse Proxy               │ ── Captures true client IP (X-Real-IP)
└──────────────────────┬───────────────────────┘
                       │  (Reverse Proxy forwarding on attacker-facing network)
                       ▼
┌──────────────────────────────────────────────┐
│          FastAPI Decoy Honeypot              │ ── Realistic WordPress / Admin decoy (/wp-login.php, etc.)
└──────────────────────┬───────────────────────┘    Returns 401 Unauthorized, redacts passwords, zero execution
                       │
                       │  (Service Auth: X-Internal-Token on isolated internal-net)
                       ▼
┌──────────────────────────────────────────────┐
│           Internal Ingest API                │ ── Authenticates decoy, validates & sanitizes payload,
└──────────────────────┬───────────────────────┘    normalizes threat schema, applies bounds checking
                       │
                       ▼  (Direct ORM writes inside internal-net)
┌──────────────────────────────────────────────┐
│       PostgreSQL Isolated Database           │ ── Network-isolated storage (Unreachable from attacker-facing net)
└──────────────────────┬───────────────────────┘
                       │
                (Read-Only queries)
                       │
┌──────────────────────┴───────────────────────┐
│             Dashboard REST API               │ ── Telemetry aggregation, timeline buckets, attacker IP profiles
└──────────────────────┬───────────────────────┘
                       │
                       ▼  (Port 3000 / Web UI)
┌──────────────────────────────────────────────┐
│          React + Vite SOC Dashboard          │ ── Live event streaming, charts, forensic inspector, IOC ledger
└──────────────────────────────────────────────┘
```

### Network Segmentation (Air-Gapped Boundaries)
1. **`attacker-facing` network**: Public bridge containing only **Nginx** and the **FastAPI Decoy**.
2. **`internal-net` network**: Private bridge containing the **Decoy**, **Ingest API**, **PostgreSQL Database**, and **Dashboard API**.
3. **No Direct Database Access**: The Decoy has no database drivers or credentials. Even if fully compromised, an adversary cannot query, modify, or erase collected threat intelligence.

---

## 🛠️ Service Summary & Port Bindings

| Service | Technology | Port (Host) | Internal Network | Purpose |
|---|---|---|---|---|
| **Nginx Proxy** | Nginx 1.25 Alpine | `80` | `attacker-facing` | Public entry point & real source IP extraction |
| **Decoy Honeypot** | Python 3.11 + FastAPI | `8000` *(Internal)* | `attacker-facing`, `internal-net` | WordPress 6.x fake portal & honeytraps |
| **Ingest API** | Python 3.11 + FastAPI | `8001` *(Internal)* | `internal-net` | Authenticated event intake & normalization |
| **PostgreSQL DB** | PostgreSQL 15 Alpine | `5432` *(Isolated)* | `internal-net` | Isolated threat intelligence persistence |
| **Dashboard API** | Python 3.11 + FastAPI | `8002` | `internal-net` | Read-only telemetry & analytics endpoints |
| **Dashboard UI** | React 18 + Vite | `3000` | `internal-net` | Real-time SOC monitoring interface |

---

## 💻 Complete Command Reference

### 1. Prerequisites Check
Before running the platform, ensure **Docker Desktop** is running:
```powershell
docker info
```

### 2. Platform Setup & Launch

#### Using Automated PowerShell Scripts (Recommended on Windows):
```powershell
# 1. Prepare environment and verify prerequisites
.\scripts\setup.ps1

# 2. Build and start all 6 services in background
.\scripts\start.ps1

# 3. Stop running services
.\scripts\stop.ps1

# 4. Clean reset (wipes database volumes & containers)
.\scripts\reset.ps1
```

#### Using Docker Compose:
```powershell
# Build all container images
docker compose build

# Start services in the background
docker compose up -d

# Start with forced rebuild
docker compose up -d --build

# View container status and health
docker compose ps

# View live streaming logs across all containers
docker compose logs -f

# View logs for a specific service
docker compose logs -f decoy
docker compose logs -f ingest
docker compose logs -f dashboard-api

# Stop all containers (preserve database)
docker compose down

# Stop containers and wipe database volumes (Full reset)
docker compose down -v --remove-orphans
```

#### Using Make (Linux / macOS / Git Bash):
```bash
make build    # Build all container images
make up       # Launch platform in background
make down     # Stop all services
make logs     # Follow container logs
make clean    # Wipe volumes and containers
make test     # Run test suite
make demo     # Run attack simulation
```

---

## 🔍 How to Test & Simulate Attacks

### A. Manual Browser Testing
1. Visit the **Decoy Web Portal**: [http://localhost/wp-login.php](http://localhost/wp-login.php)
2. Enter any test credentials (e.g., `admin` / `P@ssword123!`) and click **Log In**.
3. The decoy will return an **`HTTP 401 Unauthorized`** response without logging you in.
4. Open the **SOC Dashboard**: [http://localhost:3000](http://localhost:3000)
5. Navigate to **🚨 Live Events** to see your intercepted attack with your IP and redacted password.

### B. Automated Attack Simulation Script
Simulate realistic attacker traffic (WordPress brute force, XML-RPC floods, sensitive file exfiltration):
```powershell
# Run default simulation (8 attacks matching PDF research findings)
python .\scripts\generate_demo_events.py

# Custom attack volume and interval
python .\scripts\generate_demo_events.py --count 20 --delay 0.5 --url http://localhost:80
```

### C. Manual CLI Probing (curl)
```bash
# 1. Fake Login Attempt (Returns 401 Unauthorized)
curl -i -X POST http://localhost/wp-login.php -d "log=admin&pwd=MyPassword123"

# 2. WordPress Admin Console Probe (Returns 403 Forbidden)
curl -i http://localhost/wp-admin/

# 3. Crawler Honeytrap Probe (Returns 200 OK with bait disallows)
curl -i http://localhost/robots.txt

# 4. Environment File Exfiltration Probe (Returns 404 Not Found)
curl -i http://localhost/.env

# 5. XML-RPC Amplification Probe (Returns 403 Forbidden)
curl -i http://localhost/xmlrpc.php
```

### D. Running Integration & Unit Tests
```powershell
python -m unittest discover -s tests/integration -p "test_*.py"
```

---

## 🌐 Endpoints & URLs

- **Honeypot Decoy Portal (Attacker Entry)**: [http://localhost/wp-login.php](http://localhost/wp-login.php)
- **Honeypot Fake Corporate Site**: [http://localhost/](http://localhost/)
- **Robots.txt Honeytrap**: [http://localhost/robots.txt](http://localhost/robots.txt)
- **SOC Visibility Dashboard (Operator UI)**: [http://localhost:3000](http://localhost:3000)
- **Dashboard Telemetry API Documentation**: [http://localhost:8002/docs](http://localhost:8002/docs)
- **Dashboard Summary KPI Endpoint**: [http://localhost:8002/api/dashboard/summary](http://localhost:8002/api/dashboard/summary)
- **Dashboard Events Endpoint**: [http://localhost:8002/api/events?limit=50](http://localhost:8002/api/events?limit=50)

---

## 🔒 Security Design & Data Sanitization Principles

1. **Zero Real Execution**: The decoy has no database drivers or active administrative mechanisms. Attacker commands and SQL injections are safely logged and discarded.
2. **Password Sanitization**: Cleartext passwords submitted in forms or payloads are immediately scrubbed to `[REDACTED]` prior to internal transmission.
3. **Internal Auth Tokens**: All decoy-to-ingest communication is secured via constant-time evaluated `X-Internal-Token` headers.
4. **Denial-of-Service Defense**: Ingest limits payload sizes to 64KB, rejecting oversized memory exhaustion attempts.

---

## 📁 Repository Directory Structure

```
deception-threat-platform/
│
├── README.md                           # Master project documentation & commands
├── .env                                # Local active environment configuration
├── .env.example                        # Safe environment template
├── .gitignore                          # Ignored caches, volumes, logs
├── docker-compose.yml                  # Multi-service container orchestration
├── Makefile                            # Developer convenience shortcuts
│
├── docs/                               # System architecture & technical specs
│   ├── architecture.md                 # Trust boundaries & network design
│   ├── api-documentation.md            # Ingest & Dashboard REST API contracts
│   ├── database-schema.md              # PostgreSQL schema & indexing specification
│   ├── security-design.md              # Threat modeling & defense mitigations
│   └── testing-guide.md                # Verification & testing procedures
│
├── nginx/                              # Public Reverse Proxy
│   ├── Dockerfile                      # Nginx Alpine container definition
│   ├── nginx.conf                      # Master proxy config with honeypot logging
│   └── conf.d/
│       └── honeypot.conf               # Port 80 routing to Decoy with IP forwarding
│
├── services/
│   │
│   ├── decoy/                          # Attacker-Facing WordPress Decoy (FastAPI)
│   │   ├── Dockerfile                  # Decoy container definition
│   │   ├── requirements.txt            # FastAPI, uvicorn, jinja2, httpx
│   │   ├── app/
│   │   │   ├── main.py                 # Application entry point & route registration
│   │   │   ├── config.py               # Settings & environment validation
│   │   │   ├── routes/
│   │   │   │   ├── login.py            # Simulated WordPress /wp-login.php handler
│   │   │   │   ├── pages.py            # Fake corporate landing & /admin portal
│   │   │   │   └── probes.py           # Honeytraps: /robots.txt, /.env, /xmlrpc.php
│   │   │   ├── capture/
│   │   │   │   ├── request_capture.py  # Source IP extraction & password redactor
│   │   │   │   ├── fingerprint.py      # Non-invasive SHA-256 client fingerprinting
│   │   │   │   └── event_builder.py    # Formats standardized threat event JSON
│   │   │   ├── client/
│   │   │   │   ├── ingest_client.py    # Asynchronous event dispatcher to Ingest API
│   │   │   │   └── auth_client.py      # Injects internal service auth headers
│   │   │   └── templates/
│   │   │       ├── login.html          # High-fidelity WordPress login template
│   │   │       ├── error.html          # Generic 403 access denial template
│   │   │       └── admin.html          # Enterprise administration trap template
│   │
│   ├── ingest/                         # Internal Event Intake & Validation (FastAPI)
│   │   ├── Dockerfile                  # Ingest API container definition
│   │   ├── requirements.txt            # FastAPI, sqlalchemy, psycopg2
│   │   ├── app/
│   │   │   ├── main.py                 # Ingest application entry point
│   │   │   ├── config.py               # Ingest settings & database credentials
│   │   │   ├── api/routes/
│   │   │   │   ├── events.py           # Authenticated POST /api/v1/events
│   │   │   │   ├── health.py           # Health check endpoint
│   │   │   │   └── metrics.py          # Ingestion queue counters
│   │   │   ├── security/
│   │   │   │   ├── authentication.py   # FastAPI dependency enforcing token security
│   │   │   │   └── internal_auth.py    # Constant-time token comparison
│   │   │   ├── schemas/
│   │   │   │   ├── event_schema.py     # Pydantic schemas for event models
│   │   │   │   └── response_schema.py  # Standardized API response format
│   │   │   ├── validators/
│   │   │   │   ├── event_validator.py  # IP address & classification validation
│   │   │   │   └── payload_validator.py# Max size bounds & JSON structure check
│   │   │   ├── normalizers/
│   │   │   │   └── event_normalizer.py # UTC timestamps, trim, and field lowercasing
│   │   │   ├── services/
│   │   │   │   ├── event_service.py    # Ingestion orchestration pipeline
│   │   │   │   └── metrics_service.py  # Calculates telemetry counters
│   │   │   ├── repositories/
│   │   │   │   └── event_repository.py # Direct database access layer
│   │   │   └── database/
│   │   │       ├── connection.py       # SQLAlchemy engine & session dependency
│   │   │       └── models.py           # ThreatEvent database model definition
│   │   └── tests/
│   │       ├── test_events.py          # Unit test for event submission
│   │       ├── test_validation.py      # Unit test for validator checks
│   │       └── test_auth.py            # Unit test for token verification
│   │
│   ├── dashboard-api/                  # Read-Only Telemetry API (FastAPI)
│   │   ├── Dockerfile                  # Dashboard API container definition
│   │   ├── requirements.txt            # FastAPI, sqlalchemy, psycopg2
│   │   ├── app/
│   │   │   ├── main.py                 # API entry point & CORS configuration
│   │   │   ├── config.py               # Database URL configuration
│   │   │   ├── database.py             # Read-only SQLAlchemy connection
│   │   │   ├── routes/
│   │   │   │   ├── dashboard.py        # Summary KPI endpoint
│   │   │   │   ├── events.py           # Paginated event listing & detail lookup
│   │   │   │   ├── analytics.py        # Timeline, endpoint, and source aggregates
│   │   │   │   └── health.py           # Service health check
│   │   │   ├── services/
│   │   │   │   ├── dashboard_service.py# Formats overview metrics & events
│   │   │   │   └── analytics_service.py# Computes chart summaries
│   │   │   ├── repositories/
│   │   │   │   └── dashboard_repository.py # Read queries for dashboard
│   │   │   └── tests/
│   │   │       └── test_dashboard.py   # Unit test for dashboard API
│   │
│   ├── database/                       # PostgreSQL Database Setup
│   │   ├── init.sql                    # Initial database seed script (8 research events)
│   │   └── schema.sql                  # Canonical table definitions & indexes
│   │
│   └── dashboard-ui/                   # SOC Visibility Dashboard (React + Vite)
│       ├── Dockerfile                  # Multi-stage Node.js build & Nginx serve
│       ├── package.json                # React 18, Vite dependencies
│       ├── vite.config.js              # Vite server & port configuration
│       ├── index.html                  # HTML entry point with cyber shield icon
│       ├── src/
│       │   ├── main.jsx                # Application mount
│       │   ├── App.jsx                 # Routing & SOC console layout shell
│       │   ├── styles/
│       │   │   ├── global.css          # Cyber-dark SOC theme variables
│       │   │   └── dashboard.css       # Layout, KPI cards, table & badge styles
│       │   ├── api/
│       │   │   ├── apiClient.js        # Configured fetch client
│       │   │   ├── eventsApi.js        # API caller for event feeds
│       │   │   └── analyticsApi.js     # API caller for summary & metrics
│       │   ├── components/
│       │   │   ├── Sidebar.jsx         # Navigation menu (Overview, Live Events, etc.)
│       │   │   ├── Navbar.jsx          # Header with Live Ingestion pulse indicator
│       │   │   ├── StatCard.jsx        # Metric card component
│       │   │   ├── EventTable.jsx      # High-density threat log table
│       │   │   ├── EventDetailsModal.jsx# Forensic event inspector modal
│       │   │   ├── ActivityChart.jsx   # Timeline bar chart
│       │   │   ├── AttackMap.jsx       # Subnet distribution visualizer
│       │   │   ├── FilterBar.jsx       # Filter by IP, event type, severity
│       │   │   ├── LiveIndicator.jsx   # Pulsing green status beacon
│       │   │   └── LoadingState.jsx    # Animated loading screen
│       │   ├── pages/
│       │   │   ├── Overview.jsx        # Master SOC overview dashboard
│       │   │   ├── LiveEvents.jsx      # Real-time event log viewer
│       │   │   ├── AttackAnalysis.jsx  # Endpoint & attack vector breakdown
│       │   │   ├── IPAnalysis.jsx      # Attacker IP profiling & IOC ledger
│       │   │   └── Settings.jsx        # SOC console refresh interval options
│       │   ├── hooks/
│       │   │   ├── useEvents.js        # Real-time event fetching hook
│       │   │   └── useLiveMetrics.js   # Live metric polling hook
│       │   └── utils/
│       │       ├── formatDate.js      # Timestamp formatting helper
│       │       ├── eventLabels.js      # Human-readable attack category labels
│       │       └── severity.js         # Severity color badge styling
│
├── scripts/                            # Automation & Testing Scripts
│   ├── setup.ps1                       # Environment setup script
│   ├── start.ps1                       # One-click Docker Compose launcher
│   ├── stop.ps1                        # Stop containers script
│   ├── reset.ps1                       # Complete volume & database wipe script
│   └── generate_demo_events.py         # Synthetic adversary traffic generator
│
├── tests/                              # Integration Test Suite
│   ├── integration/
│   │   ├── test_event_pipeline.py      # Validates event schema & password redaction
│   │   └── test_service_health.py      # Validates default service port configurations
│   └── sample_data/
│       └── demo_events.json            # 8 baseline validation events from report
│
└── data/                               # Local volume mount placeholder
    └── .gitkeep
```
