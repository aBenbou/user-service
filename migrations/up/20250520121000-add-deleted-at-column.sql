-- Migration: Add deleted_at column to user_profiles
-- Created at: 2025-05-20T12:10:00

ALTER TABLE IF EXISTS user_profiles
    ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP; 