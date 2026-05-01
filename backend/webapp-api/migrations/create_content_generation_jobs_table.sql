-- Migration script to create content_generation_jobs table
-- This table stores content generation job records

-- Ensure jobstatus enum exists (should already exist from init script)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'jobstatus') THEN
        CREATE TYPE jobstatus AS ENUM ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', 'FAILED');
    END IF;
END$$;

-- Create content_generation_jobs table
CREATE TABLE IF NOT EXISTS content_generation_jobs (
    id VARCHAR PRIMARY KEY,
    brand_id VARCHAR NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
    user_input JSONB NOT NULL,
    status jobstatus NOT NULL DEFAULT 'PENDING',
    result JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Create index on brand_id for faster lookups
CREATE INDEX IF NOT EXISTS content_generation_jobs_brand_id_idx ON content_generation_jobs(brand_id);

-- Create index on status for filtering jobs by status
CREATE INDEX IF NOT EXISTS content_generation_jobs_status_idx ON content_generation_jobs(status);

-- Add trigger to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_content_generation_jobs_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_content_generation_jobs_updated_at_trigger ON content_generation_jobs;
CREATE TRIGGER update_content_generation_jobs_updated_at_trigger
    BEFORE UPDATE ON content_generation_jobs
    FOR EACH ROW
    EXECUTE FUNCTION update_content_generation_jobs_updated_at();
