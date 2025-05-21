-- Migration: Seed initial badges
-- Created at: 2025-05-21T12:00:00

-- Ensure uuid extension is available
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Insert Level 1 badge
INSERT INTO badges (id, type, name, description, requirement, created_at)
SELECT uuid_generate_v4(), 'level', 'Level 1', 'Reached level 1', '1', NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM badges WHERE type='level' AND requirement='1'
);

-- Insert Level 2 badge
INSERT INTO badges (id, type, name, description, requirement, created_at)
SELECT uuid_generate_v4(), 'level', 'Level 2', 'Reached level 2', '2', NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM badges WHERE type='level' AND requirement='2'
);

-- Insert First Points badge
INSERT INTO badges (id, type, name, description, requirement, created_at)
SELECT uuid_generate_v4(), 'achievement', 'First Points', 'Earned your first points', 'first_points', NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM badges WHERE type='achievement' AND requirement='first_points'
); 