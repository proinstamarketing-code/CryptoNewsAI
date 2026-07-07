import sqlite3

DB = "data/news.db"


def init_db():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS news(
            link TEXT PRIMARY KEY
        )
        """
    )

    conn.commit()

    conn.close()


def exists(link):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(
        "SELECT link FROM news WHERE link=?",
        (link,),
    )

    row = cur.fetchone()

    conn.close()

    return row is not None


def save(link):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO news VALUES(?)",
        (link,),
    )

    conn.commit()

    conn.close()