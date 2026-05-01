-- Migration: Add AI_GENERATED workflow type to campaign_generation_jobs
-- Run this on production BEFORE deploying the new code
-- Safe to run multiple times (all operations are idempotent)

-- Step 1: Create the campaign workflow type enum if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'campaigngenerationjobworkflowtype') THEN
        CREATE TYPE campaigngenerationjobworkflowtype AS ENUM ('STOCK_IMAGES_ONLY', 'USER_MEDIA_ONLY', 'AI_GENERATED');
    END IF;
END$$;

-- Step 2: Add AI_GENERATED value to the enum if it doesn't exist yet
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_enum
        WHERE enumtypid = 'campaigngenerationjobworkflowtype'::regtype
        AND enumlabel = 'AI_GENERATED'
    ) THEN
        ALTER TYPE campaigngenerationjobworkflowtype ADD VALUE 'AI_GENERATED';
    END IF;
END$$;

-- Step 3: Add workflow_type column to campaign_generation_jobs if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'campaign_generation_jobs'
        AND column_name = 'workflow_type'
    ) THEN
        ALTER TABLE campaign_generation_jobs
        ADD COLUMN workflow_type campaigngenerationjobworkflowtype;

        UPDATE campaign_generation_jobs
        SET workflow_type = 'STOCK_IMAGES_ONLY'
        WHERE workflow_type IS NULL;

        ALTER TABLE campaign_generation_jobs
        ALTER COLUMN workflow_type SET NOT NULL;
    END IF;
END$$;

-- Step 4: Create contenttype enum if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'contenttype') THEN
        CREATE TYPE contenttype AS ENUM ('TEXT', 'TEXT_WITH_SINGLE_IMAGE');
    END IF;
END$$;

-- Step 5: Create content_generation_jobs table if it doesn't exist
CREATE TABLE IF NOT EXISTS content_generation_jobs (
    id VARCHAR PRIMARY KEY,
    brand_id VARCHAR REFERENCES brands(id) ON DELETE CASCADE,
    user_input JSONB NOT NULL,
    content_type contenttype NOT NULL,
    status jobstatus NOT NULL DEFAULT 'PENDING',
    result JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS content_generation_jobs_brand_id_idx ON content_generation_jobs(brand_id);
CREATE INDEX IF NOT EXISTS content_generation_jobs_status_idx ON content_generation_jobs(status);

-- Step 6: Change user_input and result columns from JSON to JSONB if needed
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'campaign_generation_jobs'
        AND column_name = 'user_input'
        AND data_type = 'json'
    ) THEN
        ALTER TABLE campaign_generation_jobs
        ALTER COLUMN user_input TYPE JSONB USING user_input::JSONB;
    END IF;

    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'campaign_generation_jobs'
        AND column_name = 'result'
        AND data_type = 'json'
    ) THEN
        ALTER TABLE campaign_generation_jobs
        ALTER COLUMN result TYPE JSONB USING result::JSONB;
    END IF;
END$$;
