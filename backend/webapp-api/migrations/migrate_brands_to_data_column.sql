-- Migration script to move brand fields into the data jsonb column
-- This script preserves existing data and moves it into the structured data field
-- It also normalizes enum values to uppercase to match Pydantic expectations

-- Helper function to normalize archetype keys to uppercase
CREATE OR REPLACE FUNCTION normalize_archetype_mix(archetype_mix_json jsonb)
RETURNS jsonb AS $$
DECLARE
    result jsonb := '{}'::jsonb;
    key text;
    value numeric;
BEGIN
    IF archetype_mix_json IS NULL THEN
        RETURN NULL;
    END IF;
    
    FOR key, value IN SELECT * FROM jsonb_each_text(archetype_mix_json)
    LOOP
        result := result || jsonb_build_object(UPPER(key), value::numeric);
    END LOOP;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Helper function to normalize tone of voice keys to uppercase
CREATE OR REPLACE FUNCTION normalize_tone_of_voice(tone_json jsonb)
RETURNS jsonb AS $$
DECLARE
    result jsonb := '{}'::jsonb;
    key text;
    value numeric;
BEGIN
    IF tone_json IS NULL THEN
        RETURN NULL;
    END IF;
    
    FOR key, value IN SELECT * FROM jsonb_each_text(tone_json)
    LOOP
        result := result || jsonb_build_object(UPPER(key), value::numeric);
    END LOOP;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Step 1: Update existing records to populate the data column
UPDATE public.brands
SET data = jsonb_build_object(
    'description', COALESCE(description, NULL),
    'brand_mission', COALESCE(brand_mission, NULL),
    'colors', CASE 
        WHEN colors IS NOT NULL THEN colors::jsonb 
        ELSE NULL 
    END,
    'logo_url', COALESCE(logo_url, NULL),
    'media_urls', CASE 
        WHEN media_urls IS NOT NULL THEN to_jsonb(media_urls) 
        ELSE NULL 
    END,
    'audience_description', COALESCE(audience_description, NULL),
    'business_description', COALESCE(business_description, NULL),
    'branding_description', COALESCE(branding_description, NULL),
    'marketing_description', COALESCE(marketing_description, NULL),
    'archetype', CASE 
        WHEN archetype IS NOT NULL THEN UPPER(archetype)
        ELSE NULL 
    END,
    'archetype_mix', CASE 
        WHEN archetype_mix IS NOT NULL THEN normalize_archetype_mix(archetype_mix::jsonb)
        ELSE NULL 
    END,
    'tone_of_voice', CASE 
        WHEN tone_of_voice IS NOT NULL THEN normalize_tone_of_voice(tone_of_voice::jsonb)
        ELSE NULL 
    END
)
WHERE data IS NULL OR data = '{}'::jsonb;

-- Step 2: For records that already have data, normalize and merge
UPDATE public.brands
SET data = data || jsonb_build_object(
    'description', COALESCE(description, data->>'description'),
    'brand_mission', COALESCE(brand_mission, data->>'brand_mission'),
    'colors', CASE 
        WHEN colors IS NOT NULL THEN colors::jsonb 
        WHEN data->'colors' IS NOT NULL THEN data->'colors'
        ELSE NULL 
    END,
    'logo_url', COALESCE(logo_url, data->>'logo_url'),
    'media_urls', CASE 
        WHEN media_urls IS NOT NULL THEN to_jsonb(media_urls)
        WHEN data->'media_urls' IS NOT NULL THEN data->'media_urls'
        ELSE NULL 
    END,
    'audience_description', COALESCE(audience_description, data->>'audience_description'),
    'business_description', COALESCE(business_description, data->>'business_description'),
    'branding_description', COALESCE(branding_description, data->>'branding_description'),
    'marketing_description', COALESCE(marketing_description, data->>'marketing_description'),
    'archetype', CASE 
        WHEN archetype IS NOT NULL THEN UPPER(archetype)
        WHEN data->>'archetype' IS NOT NULL THEN UPPER(data->>'archetype')
        ELSE NULL 
    END,
    'archetype_mix', CASE 
        WHEN archetype_mix IS NOT NULL THEN normalize_archetype_mix(archetype_mix::jsonb)
        WHEN data->'archetype_mix' IS NOT NULL THEN normalize_archetype_mix(data->'archetype_mix')
        ELSE NULL 
    END,
    'tone_of_voice', CASE 
        WHEN tone_of_voice IS NOT NULL THEN normalize_tone_of_voice(tone_of_voice::jsonb)
        WHEN data->'tone_of_voice' IS NOT NULL THEN normalize_tone_of_voice(data->'tone_of_voice')
        ELSE NULL 
    END
)
WHERE data IS NOT NULL AND data != '{}'::jsonb;

-- Step 2b: Fix existing data that already has lowercase enum values
UPDATE public.brands
SET data = jsonb_set(
    jsonb_set(
        jsonb_set(
            data,
            '{archetype}',
            to_jsonb(UPPER(data->>'archetype'))
        ),
        '{archetype_mix}',
        normalize_archetype_mix(data->'archetype_mix')
    ),
    '{tone_of_voice}',
    normalize_tone_of_voice(data->'tone_of_voice')
)
WHERE data IS NOT NULL 
  AND (
    data->>'archetype' IS NOT NULL 
    OR data->'archetype_mix' IS NOT NULL 
    OR data->'tone_of_voice' IS NOT NULL
  );

-- Step 3: Drop the old columns (uncomment when ready to execute)
-- Note: This is commented out for safety. Uncomment and run after verifying the migration

-- -- Drop foreign key constraint first
-- ALTER TABLE public.brands DROP CONSTRAINT IF EXISTS brands_archetype_fkey;

-- -- Drop the columns
-- ALTER TABLE public.brands DROP COLUMN IF EXISTS description;
-- ALTER TABLE public.brands DROP COLUMN IF EXISTS brand_mission;
-- ALTER TABLE public.brands DROP COLUMN IF EXISTS colors;
-- ALTER TABLE public.brands DROP COLUMN IF EXISTS logo_url;
-- ALTER TABLE public.brands DROP COLUMN IF EXISTS media_urls;
-- ALTER TABLE public.brands DROP COLUMN IF EXISTS audience_description;
-- ALTER TABLE public.brands DROP COLUMN IF EXISTS business_description;
-- ALTER TABLE public.brands DROP COLUMN IF EXISTS branding_description;
-- ALTER TABLE public.brands DROP COLUMN IF EXISTS marketing_description;
-- ALTER TABLE public.brands DROP COLUMN IF EXISTS archetype;
-- ALTER TABLE public.brands DROP COLUMN IF EXISTS archetype_mix;
-- ALTER TABLE public.brands DROP COLUMN IF EXISTS tone_of_voice;

-- Step 4: Verification queries (run these to verify the migration)
-- SELECT 
--     id,
--     name,
--     data->>'description' as description,
--     data->>'brand_mission' as brand_mission,
--     data->>'logo_url' as logo_url,
--     data->'colors' as colors
-- FROM public.brands
-- LIMIT 10;

-- SELECT COUNT(*) as total_brands, 
--        COUNT(data) as brands_with_data,
--        COUNT(CASE WHEN data->>'description' IS NOT NULL THEN 1 END) as brands_with_description
-- FROM public.brands;
