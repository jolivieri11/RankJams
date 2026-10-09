CREATE TABLE IF NOT EXISTS songs (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    image TEXT
);

CREATE TABLE IF NOT EXISTS artists (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS song_artists (
    song_id TEXT NOT NULL REFERENCES songs(id),
    artist_id TEXT NOT NULL REFERENCES artists(id),
    position INTEGER NOT NULL,
    PRIMARY KEY (song_id, artist_id)
);

CREATE TABLE IF NOT EXISTS comparisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    winner_id TEXT NOT NULL REFERENCES songs(id),
    loser_id TEXT NOT NULL REFERENCES songs(id),
    created_at TEXT NOT NULL
);