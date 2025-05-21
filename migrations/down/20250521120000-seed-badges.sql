-- Migration: Remove seeded initial badges (DOWN)
-- Created at: 2025-05-21T12:00:00

DELETE FROM badges WHERE (type='level' AND requirement IN ('1','2'))
   OR (type='achievement' AND requirement='first_points'); 