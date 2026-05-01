-- Migration: Replace STOCK_IMAGES_ONLY with AI_GENERATED in campaign generation workflow types
-- and update JSONB workflow_type values in content_generation_jobs
--
-- Run this on production BEFORE deploying the new code.
-- Safe to run multiple times (all operations are idempotent).
--
-- IMPORTANT: PostgreSQL does not support removing values from an enum type directly.
-- We recreate the enum with only the values we need.

-- =============================================================================
-- STEP 1: Add AI_GENERATED to campaigngenerationjobworkflowtype if missing
-- =============================================================================
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

-- =============================================================================
-- STEP 2: Migrate existing STOCK_IMAGES_ONLY rows to AI_GENERATED
-- =============================================================================
UPDATE campaign_generation_jobs
SET workflow_type = 'AI_GENERATED'
WHERE workflow_type = 'STOCK_IMAGES_ONLY';

-- =============================================================================
-- STEP 3: Recreate the enum without STOCK_IMAGES_ONLY
--         (PostgreSQL cannot DROP values from enums, so we swap the type)
-- =============================================================================
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM pg_enum
        WHERE enumtypid = 'campaigngenerationjobworkflowtype'::regtype
        AND enumlabel = 'STOCK_IMAGES_ONLY'
    ) THEN
        ALTER TYPE campaigngenerationjobworkflowtype RENAME TO campaigngenerationjobworkflowtype_old;

        CREATE TYPE campaigngenerationjobworkflowtype AS ENUM ('USER_MEDIA_ONLY', 'AI_GENERATED');

        ALTER TABLE campaign_generation_jobs
            ALTER COLUMN workflow_type TYPE campaigngenerationjobworkflowtype
            USING workflow_type::text::campaigngenerationjobworkflowtype;

        DROP TYPE campaigngenerationjobworkflowtype_old;
    END IF;
END$$;

-- =============================================================================
-- STEP 4: Update JSONB workflow_type values in content_generation_jobs
--         TEXT_WITH_SINGLE_IMAGE_FROM_STOCK_IMAGE -> TEXT_WITH_SINGLE_IMAGE_AI_GENERATED
-- =============================================================================
UPDATE content_generation_jobs
SET user_input = jsonb_set(user_input, '{workflow_type}', '"TEXT_WITH_SINGLE_IMAGE_AI_GENERATED"')
WHERE user_input->>'workflow_type' = 'TEXT_WITH_SINGLE_IMAGE_FROM_STOCK_IMAGE';

-- =============================================================================
-- STEP 5: Remove STOCK_IMAGES from content_generation_job_workflow_type enum if it exists
-- =============================================================================
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM pg_type WHERE typname = 'content_generation_job_workflow_type'
    ) AND EXISTS (
        SELECT 1 FROM pg_enum
        WHERE enumtypid = 'content_generation_job_workflow_type'::regtype
        AND enumlabel = 'STOCK_IMAGES'
    ) THEN
        ALTER TYPE content_generation_job_workflow_type RENAME TO content_generation_job_workflow_type_old;

        CREATE TYPE content_generation_job_workflow_type AS ENUM ('TEXT_ONLY', 'USER_MEDIA');

        DO $inner$
        DECLARE
            col_exists boolean;
        BEGIN
            SELECT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'content_generation_jobs'
                AND column_name = 'workflow_type'
            ) INTO col_exists;

            IF col_exists THEN
                ALTER TABLE content_generation_jobs
                    ALTER COLUMN workflow_type TYPE content_generation_job_workflow_type
                    USING workflow_type::text::content_generation_job_workflow_type;
            END IF;
        END$inner$;

        DROP TYPE content_generation_job_workflow_type_old;
    END IF;
END$$;
