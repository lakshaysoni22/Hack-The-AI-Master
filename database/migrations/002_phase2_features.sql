-- Add role to users table
ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'student';

-- Create mission_quiz table
CREATE TABLE IF NOT EXISTS mission_quiz (
    id TEXT PRIMARY KEY,
    mission_id TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    explanation TEXT,
    xp_reward INTEGER DEFAULT 150,
    FOREIGN KEY(mission_id) REFERENCES missions(id)
);

-- Create hints table
CREATE TABLE IF NOT EXISTS hints (
    id TEXT PRIMARY KEY,
    mission_id TEXT NOT NULL,
    hint_text TEXT NOT NULL,
    xp_cost INTEGER DEFAULT 0,
    sort_order INTEGER DEFAULT 1,
    FOREIGN KEY(mission_id) REFERENCES missions(id)
);

-- Create hint_usage table
CREATE TABLE IF NOT EXISTS hint_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    hint_id TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(hint_id) REFERENCES hints(id),
    UNIQUE(user_id, hint_id)
);
