import sqlite3
from typing import List, Dict

DB_PATH = "memory.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT,
        answer TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_memory(query: str, answer: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO memory (query, answer) VALUES (?, ?)",
        (query, answer)
    )

    conn.commit()
    conn.close()


def get_relevant_memory(query: str, limit: int = 3) -> List[Dict]:

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT query, answer
    FROM memory
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    return [{"query": r[0], "answer": r[1]} for r in rows]