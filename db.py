import os

import psycopg2


def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is required to connect to PostgreSQL.")

    return psycopg2.connect(database_url)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

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

    conn.commit()
    cursor.close()
    conn.close()
