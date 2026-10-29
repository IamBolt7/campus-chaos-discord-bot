import sqlite3

DB_NAME = "campus_chaos.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            subject_name TEXT NOT NULL,
            attended INTEGER DEFAULT 0,
            total INTEGER DEFAULT 0,
            required_percentage REAL DEFAULT 75,
            UNIQUE(user_id, subject_name)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            xp INTEGER NOT NULL DEFAULT 0,
            commands_used INTEGER NOT NULL DEFAULT 0,
            quiz_wins INTEGER NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            user_id TEXT NOT NULL,
            achievement_id TEXT NOT NULL,
            unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, achievement_id)
        )
    """)

    conn.commit()
    conn.close()

    print("✅ Database tables created successfully.")