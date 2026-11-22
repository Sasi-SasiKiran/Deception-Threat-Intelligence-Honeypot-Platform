-- PostgreSQL Database Initialization Script for Deception & Threat Intelligence Platform

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Threat Events Table
CREATE TABLE IF NOT EXISTS threat_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    source_ip VARCHAR(45) NOT NULL,
    method VARCHAR(10) NOT NULL,
    endpoint VARCHAR(512) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    user_agent VARCHAR(512),
    payload_summary JSONB DEFAULT '{}'::jsonb,
    headers JSONB DEFAULT '{}'::jsonb,
    status_code INTEGER NOT NULL,
    severity VARCHAR(20) DEFAULT 'low' NOT NULL,
    fingerprint VARCHAR(64),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Indexes for high-speed queries
CREATE INDEX IF NOT EXISTS idx_threat_events_timestamp ON threat_events (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_threat_events_source_ip ON threat_events (source_ip);
CREATE INDEX IF NOT EXISTS idx_threat_events_event_type ON threat_events (event_type);
CREATE INDEX IF NOT EXISTS idx_threat_events_endpoint ON threat_events (endpoint);
CREATE INDEX IF NOT EXISTS idx_threat_events_severity ON threat_events (severity);

-- Initial seed data matching the internship validation findings (8 events, 1 observed source)
INSERT INTO threat_events (timestamp, source_ip, method, endpoint, event_type, user_agent, payload_summary, status_code, severity, fingerprint)
VALUES
(NOW() - INTERVAL '30 minutes', '192.168.1.100', 'GET', '/robots.txt', 'path_probe', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '{"query": ""}', 404, 'low', 'a1b2c3d4e5f6'),
(NOW() - INTERVAL '25 minutes', '192.168.1.100', 'GET', '/admin', 'path_probe', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '{"query": ""}', 403, 'medium', 'a1b2c3d4e5f6'),
(NOW() - INTERVAL '20 minutes', '192.168.1.100', 'GET', '/wp-login.php', 'page_access', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '{"query": ""}', 200, 'low', 'a1b2c3d4e5f6'),
(NOW() - INTERVAL '15 minutes', '192.168.1.100', 'POST', '/wp-login.php', 'login_attempt', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '{"username": "admin", "password": "[REDACTED]"}', 401, 'high', 'a1b2c3d4e5f6'),
(NOW() - INTERVAL '14 minutes', '192.168.1.100', 'POST', '/wp-login.php', 'login_attempt', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '{"username": "administrator", "password": "[REDACTED]"}', 401, 'high', 'a1b2c3d4e5f6'),
(NOW() - INTERVAL '12 minutes', '192.168.1.100', 'POST', '/wp-login.php', 'login_attempt', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '{"username": "root", "password": "[REDACTED]"}', 401, 'high', 'a1b2c3d4e5f6'),
(NOW() - INTERVAL '10 minutes', '192.168.1.100', 'GET', '/.env', 'suspicious_request', 'curl/7.88.1', '{"query": ""}', 404, 'high', 'f7e8d9c0b1a2'),
(NOW() - INTERVAL '5 minutes', '192.168.1.100', 'GET', '/xmlrpc.php', 'path_probe', 'python-requests/2.31.0', '{"query": ""}', 403, 'medium', 'e2d1c0b9a8f7');
