-- Migration script to add workflow_type column to content_generation_jobs table
-- This adds the workflow_type enum column to the existing table

-- Create content_generation_job_workflow_type enum
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'content_generation_job_workflow_type') THEN
        CREATE TYPE content_generation_job_workflow_type AS ENUM ('TEXT_ONLY', 'USER_MEDIA', 'STOCK_IMAGES');
    END IF;
END$$;

-- Add workflow_type column to content_generation_jobs table (nullable first)
ALTER TABLE content_generation_jobs
ADD COLUMN IF NOT EXISTS workflow_type content_generation_job_workflow_type;

-- Set default value for existing rows
UPDATE content_generation_jobs
SET workflow_type = 'TEXT_ONLY'
WHERE workflow_type IS NULL;

-- Now make it NOT NULL
ALTER TABLE content_generation_jobs
ALTER COLUMN workflow_type SET NOT NULL;
