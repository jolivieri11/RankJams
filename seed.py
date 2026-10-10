import sqlite3
from pathlib import Path

songs = [
    {"id": "rolling-loud", "name": "Rolling Loud", "image": "https://i.scdn.co/image/ab67616d0000b2739382b279fa552e0fae460a85", "artists": [("nine-vicious", "Nine Vicious")]},
    {"id": "stargazing", "name": "STARGAZING", "image": "https://media.pitchfork.com/photos/5b60c32dc50e6c2e339b99fe/1:1/w_800,h_800,c_limit/Travis%20Scott_Astroworld.jpg", "artists": [("travis-scott", "Travis Scott")]},
    {"id": "fancy", "name": "Fancy", "image": "https://upload.wikimedia.org/wikipedia/en/9/9c/Drake_-_Thank_Me_Later_cover.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original", "artists": [("drake", "Drake"), ("ti", "T.I."), ("swizz-beatz", "Swizz Beatz")]},
    {"id": "neon-kitchen", "name": "Neon Kitchen", "image": "https://f4.bcbits.com/img/a4025637069_16.jpg", "artists": [("devon-hendryx", "Devon Hendryx")]},
    {"id": "new-sky", "name": "New Sky", "image": "https://thumb.wikimedia.org/wikipedia/en/thumb/7/72/SiRChasingSummer.jpg/250px-SiRChasingSummer.jpg?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail", "artists": [("sir", "SiR"), ("kadhja-bonet", "Kadhja Bonet")]},
    {"id": "mom", "name": "M.O.M", "image": "https://i.scdn.co/image/ab67616d0000b273f595e5f39c4050805de5caf5", "artists": [("isaiah-rashad", "Isaiah Rashad")]},
    {"id": "cosmo-freestyle", "name": "Cosmo Freestyle", "image": "https://upload.wikimedia.org/wikipedia/en/0/01/You_Only_Die_1nce_album_cover.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original", "artists": [("freddie-gibbs", "Freddie Gibbs")]},
    {"id": "self-control", "name": "Self Control", "image": "https://upload.wikimedia.org/wikipedia/en/a/a0/Blonde_-_Frank_Ocean.jpeg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original", "artists": [("frank-ocean", "Frank Ocean")]},
    {"id": "be-like-a-woman", "name": "Be Like a Woman", "image": "https://i5.walmartimages.com/seo/White-Trails-CD_e6059b49-5a72-4e35-99ad-b1b2f65cad9d.50054e2aa7a3df88245f55353a32858d.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF", "artists": [("chris-rainbow", "Chris Rainbow")]},
    {"id": "cinderella", "name": "Cinderella", "image": "https://upload.wikimedia.org/wikipedia/en/9/93/Mac_Miller_-_The_Divine_Feminine.png?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original", "artists": [("mac-miller", "Mac Miller"), ("ty-dolla-sign", "Ty Dolla $ign")]}
]

BASE = Path(__file__).parent

conn = sqlite3.connect(BASE / "instance" / "rankjams.db")
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON;")

with open(BASE / "schema.sql") as f:
    conn.executescript(f.read())

with conn:
    for song in songs:
        conn.execute(
            "INSERT OR IGNORE INTO songs (id, name, image) VALUES (?, ?, ?)",
            (song["id"], song["name"], song["image"])
        )
        for position, (artist_id, artist_name) in enumerate(song["artists"], start=1):
            conn.execute(
                "INSERT OR IGNORE INTO artists (id, name) VALUES (?, ?)",
                (artist_id, artist_name)
            )
            conn.execute(
                "INSERT OR IGNORE INTO song_artists (song_id, artist_id, position) VALUES (?, ?, ?)",
                (song["id"], artist_id, position)
            )


for row in conn.execute("""
    SELECT s.name, group_concat(a.name, ', ' ORDER BY sa.position) AS artists
    FROM songs s
    JOIN song_artists sa ON sa.song_id = s.id
    JOIN artists a       ON a.id = sa.artist_id
    GROUP BY s.id
"""):
    print(row["name"], "-", row["artists"])

conn.close()