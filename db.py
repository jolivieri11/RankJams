import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flask import current_app, g

SCHEMA_PATH = Path(__file__).with_name("schema.sql")

# --- Connection Handling ---
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(Path(current_app.instance_path) / "rankjams.db")
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)       # Closes connection every request
    with app.app_context():
        get_db().executescript(SCHEMA_PATH.read_text())


# --- Queries ---

def random_songs(count: int) -> list[sqlite3.Row]:
    return get_db().execute(
        "SELECT * FROM songs ORDER BY RANDOM() LIMIT ?",
        (count,)
    ).fetchall()

def record_comparison(winner_id: str, loser_id: str) -> None:
    db = get_db()
    db.execute(
        "INSERT INTO comparisons (winner_id, loser_id, created_at) VALUES (?, ?, ?)",
        (winner_id, loser_id, datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    )
    db.commit()

def song_exists(song_id: str) -> bool:
    return get_db().execute(
        "SELECT 1 FROM songs WHERE id = ?",
        (song_id,)
    ).fetchone() is not None

def top_songs(limit: int) -> list[sqlite3.Row]:
    return get_db().execute("""
        SELECT s.id, s.name, s.image,
           (SELECT group_concat(a.name, ', ' ORDER BY sa.position)
            FROM song_artists sa
            JOIN artists a ON a.id = sa.artist_id
            WHERE sa.song_id = s.id) AS artists,
        COUNT(c.id) AS wins
        FROM songs s
        JOIN comparisons c ON c.winner_id = s.id
        GROUP BY s.id
        ORDER BY wins DESC, s.name
        LIMIT ?;
        """, (limit, )).fetchall()