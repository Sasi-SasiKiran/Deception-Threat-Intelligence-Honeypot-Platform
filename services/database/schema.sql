-- PostgreSQL Reference Schema for Deception & Threat Intelligence Platform

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

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

CREATE INDEX IF NOT EXISTS idx_threat_events_timestamp ON threat_events (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_threat_events_source_ip ON threat_events (source_ip);
CREATE INDEX IF NOT EXISTS idx_threat_events_event_type ON threat_events (event_type);
CREATE INDEX IF NOT EXISTS idx_threat_events_endpoint ON threat_events (endpoint);
CREATE INDEX IF NOT EXISTS idx_threat_events_severity ON threat_events (severity);
