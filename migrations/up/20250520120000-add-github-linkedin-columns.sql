-- Migration: Add github_username and linkedin_url columns to user_profiles
-- Created at: 2025-05-20T12:00:00

ALTER TABLE IF EXISTS user_profiles
    ADD COLUMN IF NOT EXISTS github_username VARCHAR(50),
    ADD COLUMN IF NOT EXISTS linkedin_url VARCHAR(255); 