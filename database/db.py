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

    conn.commit()
    conn.close()

    print("✅ Database tables created successfully.")