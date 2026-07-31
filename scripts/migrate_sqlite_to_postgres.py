import os
import sqlite3

import psycopg2
from dotenv import load_dotenv

from db import init_db


TABLES = {
    "users": ["id", "username", "password", "bio", "goal"],
    "tasks": ["id", "username", "task", "completed", "created_at", "completed_at"],
    "journals": ["id", "username", "content", "created_at", "updated_at"],
    "moods": ["id", "username", "mood", "created_at"],
    "chat_messages": ["id", "username", "role", "message", "created_at"],
}


def table_exists(cursor, table_name):
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    )
    return cursor.fetchone() is not None


def migrate_table(sqlite_cursor, postgres_cursor, table_name, columns):
    if not table_exists(sqlite_cursor, table_name):
        return 0

    column_list = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))

    sqlite_cursor.execute(f"SELECT {column_list} FROM {table_name}")
    rows = sqlite_cursor.fetchall()

    for row in rows:
        values = list(row)

        if table_name == "tasks":
            completed_index = columns.index("completed")
            values[completed_index] = bool(values[completed_index])

        postgres_cursor.execute(
            f"""
            INSERT INTO {table_name} ({column_list})
            VALUES ({placeholders})
            ON CONFLICT (id) DO NOTHING
            """,
            values,
        )

    postgres_cursor.execute(
        """
        SELECT setval(
            pg_get_serial_sequence(%s, 'id'),
            COALESCE((SELECT MAX(id) FROM """ + table_name + """), 1),
            (SELECT COUNT(*) > 0 FROM """ + table_name + """)
        )
        """,
        (table_name,),
    )

    return len(rows)


def main():
    load_dotenv()
    init_db()

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required.")

    sqlite_path = os.getenv("SQLITE_PATH", "database.db")

    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_cursor = sqlite_conn.cursor()

    postgres_conn = psycopg2.connect(database_url)
    postgres_cursor = postgres_conn.cursor()

    migrated = {}
    for table_name, columns in TABLES.items():
        migrated[table_name] = migrate_table(
            sqlite_cursor,
            postgres_cursor,
            table_name,
            columns,
        )

    postgres_conn.commit()
    postgres_cursor.close()
    postgres_conn.close()
    sqlite_conn.close()

    for table_name, row_count in migrated.items():
        print(f"{table_name}: migrated {row_count} rows")


if __name__ == "__main__":
    main()
