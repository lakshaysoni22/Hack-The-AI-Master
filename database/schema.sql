CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS labs (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    topic TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS missions (
    id TEXT PRIMARY KEY,
    lab_id TEXT NOT NULL,
    mission_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY(lab_id) REFERENCES labs(id)
);

CREATE TABLE IF NOT EXISTS mission_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    lab_id TEXT NOT NULL,
    mission_id TEXT NOT NULL,
    status TEXT NOT NULL, -- 'LOCKED', 'AVAILABLE', 'IN PROGRESS', 'COMPLETED'
    completed_at TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(lab_id) REFERENCES labs(id),
    FOREIGN KEY(mission_id) REFERENCES missions(id),
    UNIQUE(user_id, lab_id, mission_id)
);

CREATE TABLE IF NOT EXISTS evidence (
    id TEXT PRIMARY KEY,
    lab_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY(lab_id) REFERENCES labs(id)
);

CREATE TABLE IF NOT EXISTS evidence_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    evidence_id TEXT NOT NULL,
    collected BOOLEAN DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(evidence_id) REFERENCES evidence(id),
    UNIQUE(user_id, evidence_id)
);

CREATE TABLE IF NOT EXISTS quiz_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    mission_id TEXT NOT NULL,
    answer TEXT NOT NULL,
    correct BOOLEAN NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(mission_id) REFERENCES missions(id)
);

CREATE TABLE IF NOT EXISTS mission_quiz (
    id TEXT PRIMARY KEY,
    mission_id TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    explanation TEXT,
    xp_reward INTEGER DEFAULT 150,
    FOREIGN KEY(mission_id) REFERENCES missions(id)
);

CREATE TABLE IF NOT EXISTS hints (
    id TEXT PRIMARY KEY,
    mission_id TEXT NOT NULL,
    hint_text TEXT NOT NULL,
    xp_cost INTEGER DEFAULT 0,
    sort_order INTEGER DEFAULT 1,
    FOREIGN KEY(mission_id) REFERENCES missions(id)
);

CREATE TABLE IF NOT EXISTS hint_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    hint_id TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(hint_id) REFERENCES hints(id),
    UNIQUE(user_id, hint_id)
);

CREATE TABLE IF NOT EXISTS lab_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    lab_id TEXT NOT NULL,
    score INTEGER DEFAULT 0,
    percentage INTEGER DEFAULT 0,
    status TEXT NOT NULL, -- 'AVAILABLE', 'IN PROGRESS', 'COMPLETED'
    completed_at TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(lab_id) REFERENCES labs(id),
    UNIQUE(user_id, lab_id)
);

CREATE TABLE IF NOT EXISTS flags (
    id TEXT PRIMARY KEY,
    lab_id TEXT NOT NULL,
    flag_value TEXT NOT NULL,
    FOREIGN KEY(lab_id) REFERENCES labs(id)
);

CREATE TABLE IF NOT EXISTS achievements (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS manual_labs (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    topic TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    description TEXT NOT NULL,
    target_type TEXT DEFAULT 'web',
    target_os TEXT DEFAULT 'linux'
);

CREATE TABLE IF NOT EXISTS manual_lab_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    manual_lab_id TEXT NOT NULL,
    status TEXT NOT NULL, -- 'AVAILABLE', 'IN PROGRESS', 'COMPLETED'
    score INTEGER DEFAULT 0,
    completed_at TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(manual_lab_id) REFERENCES manual_labs(id),
    UNIQUE(user_id, manual_lab_id)
);

CREATE TABLE IF NOT EXISTS manual_lab_flags (
    id TEXT PRIMARY KEY,
    manual_lab_id TEXT NOT NULL,
    flag_value TEXT NOT NULL,
    FOREIGN KEY(manual_lab_id) REFERENCES manual_labs(id)
);
