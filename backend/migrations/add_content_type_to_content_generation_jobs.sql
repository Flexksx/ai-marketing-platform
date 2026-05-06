-- Migration script to add content_type column to content_generation_jobs table
-- This adds the content_type enum column with uppercase values
-- Handles migration from lowercase to uppercase if enum already exists

-- Step 1: Create new enum with uppercase values (temporary name)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'contenttype_new') THEN
        CREATE TYPE contenttype_new AS ENUM ('TEXT', 'TEXT_WITH_SINGLE_IMAGE');
    END IF;
END$$;

-- Step 2: If old enum exists, migrate the column
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'contenttype') THEN
        -- Column might already exist, alter it to use new enum
        IF EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name = 'content_generation_jobs' 
            AND column_name = 'content_type'
        ) THEN
            -- Convert lowercase values to uppercase
            ALTER TABLE content_generation_jobs 
            ALTER COLUMN content_type TYPE contenttype_new 
            USING CASE 
                WHEN content_type::text = 'text' THEN 'TEXT'::contenttype_new
                WHEN content_type::text = 'text_with_single_image' THEN 'TEXT_WITH_SINGLE_IMAGE'::contenttype_new
                ELSE 'TEXT'::contenttype_new
            END;
        END IF;
        
        -- Drop old enum (only if no other tables use it)
        DROP TYPE IF EXISTS contenttype CASCADE;
    END IF;
END$$;

-- Step 3: Rename new enum to final name
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'contenttype_new') THEN
        ALTER TYPE contenttype_new RENAME TO contenttype;
    END IF;
END$$;

-- Step 4: Add content_type column if it doesn't exist
ALTER TABLE content_generation_jobs
ADD COLUMN IF NOT EXISTS content_type contenttype;

-- Step 5: Set default value for existing rows
UPDATE content_generation_jobs
SET content_type = 'TEXT'
WHERE content_type IS NULL;

-- Step 6: Make it NOT NULL
ALTER TABLE content_generation_jobs
ALTER COLUMN content_type SET NOT NULL;
