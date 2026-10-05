import json

# Loads listening data
def load_json(file_path) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)

# Returns most recent song name with artist
def most_recent_song(data: dict) -> str:
    if not data:
        return ""
    return f"{data['items'][0]['track']['name']} - {data['items'][0]['track']['artists'][0]['name']}"

# Returns dictionary of song plays sorted by play count in descending order
def count_plays(data: dict) -> dict:
    plays = {}
    for item in data.get('items', []):
        song_name = item['track']['name']
        song_artists = ", ".join(artist['name'] for artist in item['track']['artists'])
        song_id = item['track']['id']
        plays[f"{song_name} - {song_artists}"] = plays.get(f"{song_name} - {song_artists}", 0) + 1
    return dict(sorted(plays.items(), key=lambda item: item[1], reverse=True))

# Returns the top 5 most played artists
def most_played_artists(data: dict) -> dict:
    artists = {}
    play_counts = count_plays(data)
    for song, count in play_counts.items():
        artist_names = song.split(" - ")[1]
        artist_list = artist_names.split(", ")
        for artist in artist_list:
            artists[artist] = artists.get(artist, 0) + count
    return dict(sorted(artists.items(), key=lambda item: item[1], reverse=True)[:5])
