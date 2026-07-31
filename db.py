import os
import sqlite3


class SQLiteCursor:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, params=None):
        sqlite_query = query.replace("%s", "?")
        if params is None:
            return self.cursor.execute(sqlite_query)
        return self.cursor.execute(sqlite_query, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()


class SQLiteConnection:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def cursor(self):
        return SQLiteCursor(self.conn.cursor())

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        import psycopg2

        return psycopg2.connect(database_url)

    sqlite_path = os.getenv("SQLITE_PATH", "database.db")
    return SQLiteConnection(sqlite_path)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    if os.getenv("DATABASE_URL"):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            username TEXT,
            password TEXT,
            bio TEXT,
            goal TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id SERIAL PRIMARY KEY,
            username TEXT,
            task TEXT,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMPTZ
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS journals(
            id SERIAL PRIMARY KEY,
            username TEXT,
            content TEXT,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS moods(
            id SERIAL PRIMARY KEY,
            username TEXT,
            mood TEXT,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages(
            id SERIAL PRIMARY KEY,
            username TEXT,
            role TEXT,
            message TEXT,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )
        """)
    else:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            bio TEXT,
            goal TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            task TEXT,
            completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS journals(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS moods(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            mood TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            role TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

    conn.commit()
    cursor.close()
    conn.close()
