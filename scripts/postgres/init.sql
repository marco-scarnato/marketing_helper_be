-- CreativeHub PostgreSQL init script

CREATE TABLE IF NOT EXISTS _migrations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    applied_at TIMESTAMP DEFAULT NOW()
);
