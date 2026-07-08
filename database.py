import os
import sqlite3

DB = "data/news.db"


def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB)


def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            link TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def exists(link):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM news WHERE link=? LIMIT 1",
        (link,),
    )

    result = cur.fetchone()

    conn.close()

    return result is not None


def save(link):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO news(link)
        VALUES(?)
        """,
        (link,),
    )

    conn.commit()
    conn.close()