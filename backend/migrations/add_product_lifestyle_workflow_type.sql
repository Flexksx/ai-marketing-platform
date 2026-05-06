-- Migration: Add PRODUCT_LIFESTYLE workflow type to campaign_generation_jobs
-- Run this on production BEFORE deploying the new code
-- Safe to run multiple times (all operations are idempotent)

-- Add PRODUCT_LIFESTYLE value to the enum if it doesn't exist yet
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_enum
        WHERE enumtypid = 'campaigngenerationjobworkflowtype'::regtype
        AND enumlabel = 'PRODUCT_LIFESTYLE'
    ) THEN
        ALTER TYPE campaigngenerationjobworkflowtype ADD VALUE 'PRODUCT_LIFESTYLE';
    END IF;
END$$;
