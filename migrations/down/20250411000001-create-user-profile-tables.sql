-- Migration: Create User Profile Tables (DOWN)
-- Created at: 2025-04-11T00:00:01

-- Drop indexes
DROP INDEX IF EXISTS idx_user_profiles_username;
DROP INDEX IF EXISTS idx_user_profiles_visibility;
DROP INDEX IF EXISTS idx_expertise_areas_user_id;
DROP INDEX IF EXISTS idx_expertise_areas_domain;
DROP INDEX IF EXISTS idx_user_preferences_user_id;
DROP INDEX IF EXISTS idx_user_preferences_category_key;
DROP INDEX IF EXISTS idx_user_connections_requester_id;
DROP INDEX IF EXISTS idx_user_connections_recipient_id;
DROP INDEX IF EXISTS idx_user_connections_status;

-- Drop tables
DROP TABLE IF EXISTS user_connections;
DROP TABLE IF EXISTS user_preferences;
DROP TABLE IF EXISTS expertise_areas;
DROP TABLE IF EXISTS user_profiles;

-- Drop enum types
DROP TYPE IF EXISTS connection_status;
DROP TYPE IF EXISTS preference_category;
DROP TYPE IF EXISTS expertise_level;
DROP TYPE IF EXISTS visibility_type;