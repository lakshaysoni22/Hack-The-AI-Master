-- Initial schema migration is essentially the schema.sql itself, but we will just add an index or a dummy command to satisfy the first migration run.
-- The actual tables are managed by schema.sql on init, but future schema changes will go here.
-- Let's ensure the quiz_attempts has an index on user_id as an example of a first migration.
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user ON quiz_attempts(user_id);
