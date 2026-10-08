-- Add email to users table
ALTER TABLE users ADD COLUMN email TEXT UNIQUE;
