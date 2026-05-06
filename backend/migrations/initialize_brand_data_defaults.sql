-- Ensures every brands.data row matches the new BrandData schema so validation never fails.
-- 1) NULL or {} -> set full default.
-- 2) Old-format data (audience_description, archetype_mix, tone FORMALITY/HUMOUR keys) -> migrate to new shape.
-- 3) Already new-format -> leave unchanged.
-- Idempotent. Run manually after PR #107.

WITH default_data AS (
    SELECT jsonb_build_object(
        'logo_url', '',
        'media_urls', '[]'::jsonb,
        'colors', '[]'::jsonb,
        'brand_mission', '',
        'description', '',
        'archetype', 'EVERYMAN',
        'audiences', '[]'::jsonb,
        'tone_of_voice', jsonb_build_object(
            'formality_level', 1,
            'humour_level', 1,
            'irreverence_level', 1,
            'enthusiasm_level', 1,
            'industry_jargon_usage_level', 1,
            'sensory_keywords', '[]'::jsonb,
            'excluded_words', '[]'::jsonb,
            'signature_words', '[]'::jsonb,
            'sentence_length_preference', 'MEDIUM'
        ),
        'strategy_settings', NULL,
        'marketing_settings', NULL
    ) AS val
),
migrated_data AS (
    SELECT
        b.id,
        CASE
            WHEN b.data IS NULL OR b.data = '{}'::jsonb THEN (SELECT val FROM default_data)
            WHEN b.data ? 'audiences' AND b.data->'tone_of_voice' IS NOT NULL AND b.data->'tone_of_voice' ? 'formality_level' THEN b.data
            ELSE jsonb_build_object(
                'logo_url', COALESCE(b.data->>'logo_url', ''),
                'media_urls', COALESCE(b.data->'media_urls', '[]'::jsonb),
                'colors', COALESCE(b.data->'colors', '[]'::jsonb),
                'brand_mission', COALESCE(b.data->>'brand_mission', ''),
                'description', COALESCE(b.data->>'description', ''),
                'archetype', COALESCE(NULLIF(UPPER(TRIM(b.data->>'archetype')), ''), 'EVERYMAN'),
                'audiences', CASE
                    WHEN b.data->'audiences' IS NOT NULL AND jsonb_typeof(b.data->'audiences') = 'array' THEN b.data->'audiences'
                    WHEN b.data->>'audience_description' IS NOT NULL AND TRIM(b.data->>'audience_description') != '' THEN jsonb_build_array(jsonb_build_object('name', 'Primary', 'description', b.data->>'audience_description'))
                    ELSE '[]'::jsonb
                END,
                'tone_of_voice', jsonb_build_object(
                    'formality_level', COALESCE(
                        CASE WHEN (b.data->'tone_of_voice'->>'formality_level')::numeric BETWEEN 0 AND 1 THEN LEAST(4, GREATEST(1, ROUND(1 + (b.data->'tone_of_voice'->>'formality_level')::numeric * 3)::int))
                             WHEN (b.data->'tone_of_voice'->>'formality_level')::numeric IS NOT NULL THEN LEAST(4, GREATEST(1, ROUND((b.data->'tone_of_voice'->>'formality_level')::numeric)::int))
                             WHEN (b.data->'tone_of_voice'->>'FORMALITY')::numeric BETWEEN 0 AND 1 THEN LEAST(4, GREATEST(1, ROUND(1 + (b.data->'tone_of_voice'->>'FORMALITY')::numeric * 3)::int))
                             WHEN (b.data->'tone_of_voice'->>'FORMALITY')::numeric IS NOT NULL THEN LEAST(4, GREATEST(1, ROUND((b.data->'tone_of_voice'->>'FORMALITY')::numeric)::int))
                             ELSE NULL END, 1),
                    'humour_level', COALESCE(
                        CASE WHEN (b.data->'tone_of_voice'->>'humour_level')::numeric BETWEEN 0 AND 1 THEN LEAST(4, GREATEST(1, ROUND(1 + (b.data->'tone_of_voice'->>'humour_level')::numeric * 3)::int))
                             WHEN (b.data->'tone_of_voice'->>'humour_level')::numeric IS NOT NULL THEN LEAST(4, GREATEST(1, ROUND((b.data->'tone_of_voice'->>'humour_level')::numeric)::int))
                             WHEN (b.data->'tone_of_voice'->>'HUMOUR')::numeric BETWEEN 0 AND 1 THEN LEAST(4, GREATEST(1, ROUND(1 + (b.data->'tone_of_voice'->>'HUMOUR')::numeric * 3)::int))
                             WHEN (b.data->'tone_of_voice'->>'HUMOUR')::numeric IS NOT NULL THEN LEAST(4, GREATEST(1, ROUND((b.data->'tone_of_voice'->>'HUMOUR')::numeric)::int))
                             ELSE NULL END, 1),
                    'irreverence_level', COALESCE(
                        CASE WHEN (b.data->'tone_of_voice'->>'irreverence_level')::numeric BETWEEN 0 AND 1 THEN LEAST(4, GREATEST(1, ROUND(1 + (b.data->'tone_of_voice'->>'irreverence_level')::numeric * 3)::int))
                             WHEN (b.data->'tone_of_voice'->>'irreverence_level')::numeric IS NOT NULL THEN LEAST(4, GREATEST(1, ROUND((b.data->'tone_of_voice'->>'irreverence_level')::numeric)::int))
                             WHEN (b.data->'tone_of_voice'->>'IRREVERENCE')::numeric BETWEEN 0 AND 1 THEN LEAST(4, GREATEST(1, ROUND(1 + (b.data->'tone_of_voice'->>'IRREVERENCE')::numeric * 3)::int))
                             WHEN (b.data->'tone_of_voice'->>'IRREVERENCE')::numeric IS NOT NULL THEN LEAST(4, GREATEST(1, ROUND((b.data->'tone_of_voice'->>'IRREVERENCE')::numeric)::int))
                             ELSE NULL END, 1),
                    'enthusiasm_level', COALESCE(
                        CASE WHEN (b.data->'tone_of_voice'->>'enthusiasm_level')::numeric BETWEEN 0 AND 1 THEN LEAST(4, GREATEST(1, ROUND(1 + (b.data->'tone_of_voice'->>'enthusiasm_level')::numeric * 3)::int))
                             WHEN (b.data->'tone_of_voice'->>'enthusiasm_level')::numeric IS NOT NULL THEN LEAST(4, GREATEST(1, ROUND((b.data->'tone_of_voice'->>'enthusiasm_level')::numeric)::int))
                             WHEN (b.data->'tone_of_voice'->>'ENTHUSIASM')::numeric BETWEEN 0 AND 1 THEN LEAST(4, GREATEST(1, ROUND(1 + (b.data->'tone_of_voice'->>'ENTHUSIASM')::numeric * 3)::int))
                             WHEN (b.data->'tone_of_voice'->>'ENTHUSIASM')::numeric IS NOT NULL THEN LEAST(4, GREATEST(1, ROUND((b.data->'tone_of_voice'->>'ENTHUSIASM')::numeric)::int))
                             ELSE NULL END, 1),
                    'industry_jargon_usage_level', COALESCE(
                        CASE WHEN (b.data->'tone_of_voice'->>'industry_jargon_usage_level')::numeric BETWEEN 0 AND 1 THEN LEAST(4, GREATEST(1, ROUND(1 + (b.data->'tone_of_voice'->>'industry_jargon_usage_level')::numeric * 3)::int))
                             WHEN (b.data->'tone_of_voice'->>'industry_jargon_usage_level')::numeric IS NOT NULL THEN LEAST(4, GREATEST(1, ROUND((b.data->'tone_of_voice'->>'industry_jargon_usage_level')::numeric)::int))
                             ELSE NULL END, 1),
                    'sensory_keywords', COALESCE(b.data->'tone_of_voice'->'sensory_keywords', '[]'::jsonb),
                    'excluded_words', COALESCE(b.data->'tone_of_voice'->'excluded_words', '[]'::jsonb),
                    'signature_words', COALESCE(b.data->'tone_of_voice'->'signature_words', '[]'::jsonb),
                    'sentence_length_preference', CASE WHEN b.data->'tone_of_voice'->>'sentence_length_preference' IN ('SHORT', 'MEDIUM', 'LONG') THEN b.data->'tone_of_voice'->>'sentence_length_preference' ELSE 'MEDIUM' END
                ),
                'strategy_settings', NULL,
                'marketing_settings', NULL
            )
        END AS new_data
    FROM public.brands b
)
UPDATE public.brands b
SET data = m.new_data
FROM migrated_data m
WHERE b.id = m.id
  AND (
      b.data IS NULL
      OR b.data = '{}'::jsonb
      OR NOT (b.data ? 'audiences' AND b.data->'tone_of_voice' IS NOT NULL AND b.data->'tone_of_voice' ? 'formality_level')
  );
