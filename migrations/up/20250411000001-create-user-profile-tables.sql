-- Migration: Create User Profile Tables
-- Created at: 2025-04-11T00:00:01

-- Create enum types
CREATE TYPE visibility_type AS ENUM ('PUBLIC', 'PRIVATE', 'CONNECTIONS_ONLY');
CREATE TYPE expertise_level AS ENUM ('BEGINNER', 'INTERMEDIATE', 'EXPERT');
CREATE TYPE preference_category AS ENUM ('NOTIFICATIONS', 'PRIVACY', 'APPEARANCE');
CREATE TYPE connection_status AS ENUM ('PENDING', 'ACCEPTED', 'REJECTED');

-- Create user_profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(50) UNIQUE,
    biography TEXT,
    profession VARCHAR(100),
    company VARCHAR(100),
    current_job VARCHAR(100),
    github_username VARCHAR(50),
    linkedin_url VARCHAR(255),
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    visibility visibility_type DEFAULT 'PUBLIC',
    deleted_at TIMESTAMP
);

-- Create expertise_areas table
CREATE TABLE IF NOT EXISTS expertise_areas (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    domain VARCHAR(100) NOT NULL,
    level expertise_level NOT NULL,
    years_experience INTEGER,
    CONSTRAINT unique_user_domain UNIQUE (user_id, domain)
);

-- Create user_preferences table
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    category preference_category NOT NULL,
    key VARCHAR(100) NOT NULL,
    value JSONB,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_preference UNIQUE (user_id, category, key)
);

-- Create user_connections table
CREATE TABLE IF NOT EXISTS user_connections (
    id UUID PRIMARY KEY,
    requester_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    recipient_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    status connection_status DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_connection UNIQUE (requester_id, recipient_id)
);

-- Create indexes
CREATE INDEX idx_user_profiles_username ON user_profiles(username);
CREATE INDEX idx_user_profiles_visibility ON user_profiles(visibility);
CREATE INDEX idx_expertise_areas_user_id ON expertise_areas(user_id);
CREATE INDEX idx_expertise_areas_domain ON expertise_areas(domain);
CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);
CREATE INDEX idx_user_preferences_category_key ON user_preferences(category, key);
CREATE INDEX idx_user_connections_requester_id ON user_connections(requester_id);
CREATE INDEX idx_user_connections_recipient_id ON user_connections(recipient_id);
CREATE INDEX idx_user_connections_status ON user_connections(status);