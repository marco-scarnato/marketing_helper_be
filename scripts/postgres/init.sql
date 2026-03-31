-- CreativeHub PostgreSQL init script

CREATE TABLE IF NOT EXISTS _migrations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    applied_at TIMESTAMP DEFAULT NOW()
);

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(255),
    website VARCHAR(500),
    links JSONB DEFAULT '[]'::jsonb,
    contacts JSONB DEFAULT '[]'::jsonb,
    notes TEXT,
    logo_path VARCHAR(500),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_clients_status ON clients(status);
CREATE INDEX IF NOT EXISTS idx_clients_name ON clients(name);
