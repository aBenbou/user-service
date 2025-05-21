-- Migration: Remove github_username and linkedin_url columns from user_profiles (DOWN)
-- Created at: 2025-05-20T12:00:00

ALTER TABLE IF EXISTS user_profiles
    DROP COLUMN IF EXISTS github_username,
    DROP COLUMN IF EXISTS linkedin_url; 