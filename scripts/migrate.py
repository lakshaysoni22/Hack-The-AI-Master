import sqlite3
import os

DATABASE = 'database/hacktheai.db'
MIGRATIONS_DIR = 'database/migrations'

def migrate():
    if not os.path.exists(DATABASE):
        print("Database not found, please initialize first.")
        return
        
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Create migrations table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    if not os.path.exists(MIGRATIONS_DIR):
        os.makedirs(MIGRATIONS_DIR)
        print("Created migrations directory.")
        
    migrations = sorted(os.listdir(MIGRATIONS_DIR))
    
    for filename in migrations:
        if filename.endswith('.sql'):
            # Check if applied
            c.execute("SELECT id FROM migrations WHERE filename = ?", (filename,))
            if not c.fetchone():
                print(f"Applying migration {filename}...")
                filepath = os.path.join(MIGRATIONS_DIR, filename)
                with open(filepath, 'r') as f:
                    script = f.read()
                    c.executescript(script)
                c.execute("INSERT INTO migrations (filename) VALUES (?)", (filename,))
                conn.commit()
                print(f"Successfully applied {filename}.")
            else:
                print(f"Migration {filename} already applied.")
                
    conn.close()

if __name__ == '__main__':
    migrate()
