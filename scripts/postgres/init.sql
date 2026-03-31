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

CREATE TABLE IF NOT EXISTS brand_identities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL UNIQUE REFERENCES clients(id) ON DELETE CASCADE,
    business_description TEXT DEFAULT '',
    mission TEXT DEFAULT '',
    vision TEXT DEFAULT '',
    unique_value_proposition TEXT DEFAULT '',
    logos JSONB DEFAULT '[]'::jsonb,
    tone_of_voice JSONB DEFAULT '{}'::jsonb,
    visual_identity JSONB DEFAULT '{}'::jsonb,
    target_audience JSONB DEFAULT '{}'::jsonb,
    competitors JSONB DEFAULT '[]'::jsonb,
    differentiators JSONB DEFAULT '[]'::jsonb,
    products_services JSONB DEFAULT '[]'::jsonb,
    keywords_seo JSONB DEFAULT '[]'::jsonb,
    approved_claims JSONB DEFAULT '[]'::jsonb,
    restricted_topics JSONB DEFAULT '[]'::jsonb,
    legal_notes TEXT DEFAULT '',
    cta_primary TEXT DEFAULT '',
    cta_secondary TEXT DEFAULT '',
    preferred_channels JSONB DEFAULT '[]'::jsonb,
    ai_last_prompt TEXT,
    ai_last_response TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE brand_identities ADD COLUMN IF NOT EXISTS business_description TEXT DEFAULT '';
ALTER TABLE brand_identities ADD COLUMN IF NOT EXISTS mission TEXT DEFAULT '';
ALTER TABLE brand_identities ADD COLUMN IF NOT EXISTS vision TEXT DEFAULT '';
ALTER TABLE brand_identities ADD COLUMN IF NOT EXISTS unique_value_proposition TEXT DEFAULT '';
ALTER TABLE brand_identities ADD COLUMN IF NOT EXISTS visual_identity JSONB DEFAULT '{}'::jsonb;
ALTER TABLE brand_identities ADD COLUMN IF NOT EXISTS competitors JSONB DEFAULT '[]'::jsonb;
ALTER TABLE brand_identities ADD COLUMN IF NOT EXISTS differentiators JSONB DEFAULT '[]'::jsonb;
ALTER TABLE brand_identities ADD COLUMN IF NOT EXISTS products_services JSONB DEFAULT '[]'::jsonb;
ALTER TABLE brand_identities ADD COLUMN IF NOT EXISTS keywords_seo JSONB DEFAULT '[]'::jsonb;
ALTER TABLE brand_identities ADD COLUMN IF NOT EXISTS approved_claims JSONB DEFAULT '[]'::jsonb;
ALTER TABLE brand_identities ADD COLUMN IF NOT EXISTS restricted_topics JSONB DEFAULT '[]'::jsonb;
ALTER TABLE brand_identities ADD COLUMN IF NOT EXISTS legal_notes TEXT DEFAULT '';
ALTER TABLE brand_identities ADD COLUMN IF NOT EXISTS cta_primary TEXT DEFAULT '';
ALTER TABLE brand_identities ADD COLUMN IF NOT EXISTS cta_secondary TEXT DEFAULT '';
ALTER TABLE brand_identities ADD COLUMN IF NOT EXISTS preferred_channels JSONB DEFAULT '[]'::jsonb;

CREATE INDEX IF NOT EXISTS idx_brand_identities_client_id ON brand_identities(client_id);
