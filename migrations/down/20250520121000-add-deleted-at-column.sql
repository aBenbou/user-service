-- Migration: Remove deleted_at column from user_profiles (DOWN)
-- Created at: 2025-05-20T12:10:00

ALTER TABLE IF EXISTS user_profiles
    DROP COLUMN IF EXISTS deleted_at; 