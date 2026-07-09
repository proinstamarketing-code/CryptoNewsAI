import sqlite3
from pathlib import Path

# Папка для базы данных
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "news.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    """Создает базу и таблицу при первом запуске."""

    with get_connection() as conn:

        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS news (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            link TEXT UNIQUE,

            title TEXT,

            category TEXT,

            published_at TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        conn.commit()


def exists(link: str) -> bool:
    """Проверяем, публиковали ли уже новость."""

    with get_connection() as conn:

        cur = conn.cursor()

        cur.execute(
            "SELECT 1 FROM news WHERE link = ?",
            (link,)
        )

        return cur.fetchone() is not None


def save(
    link: str,
    title: str = "",
    category: str = "",
    published_at: str = "",
):
    """Сохраняем опубликованную новость."""

    with get_connection() as conn:

        cur = conn.cursor()

        cur.execute("""
        INSERT OR IGNORE INTO news (
            link,
            title,
            category,
            published_at
        )
        VALUES (?, ?, ?, ?)
        """, (
            link,
            title,
            category,
            published_at,
        ))

        conn.commit()


def stats():

    with get_connection() as conn:

        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM news")

        return cur.fetchone()[0]