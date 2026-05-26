import json
import os
import sqlite3
from pathlib import Path
from typing import Optional

from .models import StudentProgress


def _db_path() -> Path:
    return Path(os.getenv("SKILLWIZ_DB_PATH", "data/skillwiz.db"))


def _seed_path() -> Path:
    return Path("data/seed.json")


def ensure_db() -> None:
    path = _db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                user_id TEXT PRIMARY KEY,
                target TEXT NOT NULL,
                current_phase TEXT NOT NULL,
                completed_topics TEXT NOT NULL,
                pending_topics TEXT NOT NULL,
                streak INTEGER NOT NULL
            )
            """
        )
        if _is_empty(conn):
            _seed_data(conn)


def _is_empty(conn: sqlite3.Connection) -> bool:
    row = conn.execute("SELECT COUNT(*) FROM students").fetchone()
    return row is not None and row[0] == 0


def _seed_data(conn: sqlite3.Connection) -> None:
    seed_path = _seed_path()
    if not seed_path.exists():
        return
    data = json.loads(seed_path.read_text(encoding="utf-8"))
    for item in data:
        conn.execute(
            """
            INSERT OR REPLACE INTO students (
                user_id, target, current_phase, completed_topics, pending_topics, streak
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                item["user_id"],
                item["target"],
                item["current_phase"],
                json.dumps(item["completed_topics"]),
                json.dumps(item["pending_topics"]),
                int(item["streak"]),
            ),
        )


def get_student_progress(user_id: str) -> Optional[StudentProgress]:
    ensure_db()
    path = _db_path()
    with sqlite3.connect(path) as conn:
        row = conn.execute(
            """
            SELECT user_id, target, current_phase, completed_topics, pending_topics, streak
            FROM students WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()
    if not row:
        return None
    completed = json.loads(row[3])
    pending = json.loads(row[4])
    return StudentProgress(
        user_id=row[0],
        target=row[1],
        current_phase=row[2],
        completed_topics=completed,
        pending_topics=pending,
        streak=int(row[5]),
    )
