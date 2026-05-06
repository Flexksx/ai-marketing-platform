-- Initialize local development database with base schema
-- This script creates all required tables for the backend application
-- Run this BEFORE running Alembic migrations

-- Create ENUM types
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'jobstatus') THEN
        CREATE TYPE jobstatus AS ENUM ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', 'FAILED');
    END IF;
END$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'postchannel') THEN
        CREATE TYPE postchannel AS ENUM ('INSTAGRAM', 'LINKEDIN');
    END IF;
END$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'contentchannelname') THEN
        CREATE TYPE contentchannelname AS ENUM ('INSTAGRAM', 'LINKEDIN');
    END IF;
END$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'campaignstate') THEN
        CREATE TYPE campaignstate AS ENUM ('DRAFT', 'LIVE', 'PAUSED', 'ENDED');
    END IF;
END$$;

-- Create brand_archetypes table (no foreign keys)
CREATE TABLE IF NOT EXISTS brand_archetypes (
    name VARCHAR PRIMARY KEY,
    base_human_need TEXT NOT NULL,
    archetype_description TEXT NOT NULL,
    identification_clues TEXT NOT NULL,
    core_shared_values TEXT NOT NULL,
    typical_target_audience TEXT NOT NULL,
    colors_graphics_description TEXT NOT NULL,
    writing_style_description TEXT NOT NULL,
    examples TEXT NOT NULL
);

-- Create tone_of_voice_dimensions table (no foreign keys)
CREATE TABLE IF NOT EXISTS tone_of_voice_dimensions (
    name VARCHAR PRIMARY KEY,
    left_extreme_description TEXT NOT NULL,
    left_extreme_wording TEXT NOT NULL,
    left_extreme_audience_fit TEXT NOT NULL,
    left_extreme_values TEXT NOT NULL,
    left_extreme_indicators TEXT NOT NULL,
    left_extreme_best_practices TEXT NOT NULL,
    right_extreme_description TEXT NOT NULL,
    right_extreme_wording TEXT NOT NULL,
    right_extreme_audience_fit TEXT NOT NULL,
    right_extreme_values TEXT NOT NULL,
    right_extreme_indicators TEXT NOT NULL,
    right_extreme_best_practices TEXT NOT NULL
);

-- Create brands table (depends on brand_archetypes)
CREATE TABLE IF NOT EXISTS brands (
    id VARCHAR PRIMARY KEY,
    user_id TEXT NOT NULL DEFAULT '',
    name TEXT NOT NULL,
    description TEXT,
    brand_mission TEXT,
    colors JSON,
    logo_url TEXT,
    media_urls TEXT[],
    audience_description TEXT,
    business_description TEXT,
    branding_description TEXT,
    marketing_description TEXT,
    archetype VARCHAR REFERENCES brand_archetypes(name),
    archetype_mix JSON,
    tone_of_voice JSON,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
CREATE INDEX IF NOT EXISTS brands_supabaseUserId_idx ON brands(user_id);

-- Create brand_generation_jobs table (no foreign keys to other tables)
CREATE TABLE IF NOT EXISTS brand_generation_jobs (
    id VARCHAR PRIMARY KEY,
    status jobstatus NOT NULL DEFAULT 'PENDING',
    website_url VARCHAR NOT NULL,
    extra_routes VARCHAR[] NOT NULL DEFAULT ARRAY['/about', '/help'],
    result JSON,
    user_id VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create campaigns table (depends on brands)
CREATE TABLE IF NOT EXISTS campaigns (
    id VARCHAR PRIMARY KEY,
    brand_id VARCHAR REFERENCES brands(id),
    topic VARCHAR,
    goal VARCHAR,
    target_audience VARCHAR,
    content_pillar VARCHAR,
    description VARCHAR,
    duration_days INTEGER,
    channels contentchannelname[],
    state campaignstate,
    media_urls VARCHAR[],
    started_at TIMESTAMP WITH TIME ZONE,
    paused_at TIMESTAMP WITH TIME ZONE,
    ended_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS campaigns_brand_id_idx ON campaigns(brand_id);
CREATE INDEX IF NOT EXISTS campaigns_state_idx ON campaigns(state);

-- Create campaign_generation_job_workflow_type enum
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'campaigngenerationjobworkflowtype') THEN
        CREATE TYPE campaigngenerationjobworkflowtype AS ENUM ('USER_MEDIA_ONLY', 'AI_GENERATED');
    END IF;
END$$;

-- Create contenttype enum
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'contenttype') THEN
        CREATE TYPE contenttype AS ENUM ('TEXT', 'TEXT_WITH_SINGLE_IMAGE');
    END IF;
END$$;

-- Create campaign_generation_jobs table (depends on brands)
CREATE TABLE IF NOT EXISTS campaign_generation_jobs (
    id VARCHAR PRIMARY KEY,
    brand_id VARCHAR REFERENCES brands(id) ON DELETE CASCADE,
    workflow_type campaigngenerationjobworkflowtype NOT NULL,
    user_input JSONB NOT NULL,
    status jobstatus NOT NULL DEFAULT 'PENDING',
    result JSONB,
    version INTEGER DEFAULT 0 NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create content_generation_jobs table (depends on brands)
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

-- Create posts table (depends on campaigns)
CREATE TABLE IF NOT EXISTS posts (
    id VARCHAR PRIMARY KEY,
    campaign_id VARCHAR REFERENCES campaigns(id) ON DELETE CASCADE,
    channel contentchannelname,
    caption TEXT,
    media_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    scheduled_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS posts_campaignId_idx ON posts(campaign_id);
CREATE INDEX IF NOT EXISTS posts_scheduled_at_idx ON posts(scheduled_at);

-- Create post_generation_jobs table (depends on campaign_generation_jobs)
CREATE TABLE IF NOT EXISTS post_generation_jobs (
    id VARCHAR PRIMARY KEY,
    campaign_generation_job_id VARCHAR NOT NULL REFERENCES campaign_generation_jobs(id),
    image_url VARCHAR,
    topic VARCHAR NOT NULL,
    channel contentchannelname NOT NULL,
    scheduled_at TIMESTAMP WITH TIME ZONE NOT NULL,
    status jobstatus NOT NULL DEFAULT 'PENDING',
    assigned_image_url VARCHAR,
    result JSON,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_post_generation_jobs_campaign_generation_job_id ON post_generation_jobs(campaign_generation_job_id);

-- Create alembic_version table to mark migrations as applied
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) PRIMARY KEY
);

-- Mark all existing migrations as applied since we created the schema from scratch
-- This prevents Alembic from trying to re-run migrations that would fail
INSERT INTO alembic_version (version_num) VALUES ('ee2c545616c7')
ON CONFLICT (version_num) DO NOTHING;

-- =====================================================
-- SEED DATA
-- =====================================================

DO $$ BEGIN RAISE NOTICE 'Local development database initialized successfully!'; END $$;
