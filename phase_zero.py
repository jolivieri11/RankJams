import json

# Loads listening data
def load_json(file_path) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)

# Returns most recent song name with artist
def most_recent_song(data: dict) -> str:
    if not data:
        return ""
    return f"{data['items'][0]['track']['name']} - {', '.join(
        artist['name'] for artist in data['items'][0]['track']['artists'])}"

# Returns dictionary of song plays sorted by play count in descending order
def count_plays(data: dict) -> dict:
    plays = {}
    if not data:
        return plays
    for item in data.get('items', []):
        song_id = item['track']['id']
        plays[f"{song_id}"] = plays.get(f"{song_id}", 0) + 1
    return dict(sorted(plays.items(), key=lambda item: item[1], reverse=True))

# Returns the top 5 most played artists
def most_played_artists(data: dict) -> dict:
    artists = {}
    if not data:
        return artists
    for item in data['items']:
        for artist in item['track']['artists']:
            artist_name = artist['name']
            artists[artist_name] = artists.get(artist_name, 0) + 1
    return dict(sorted(artists.items(), key=lambda item: item[1], reverse=True)[:5])

data = load_json('listening_history.json')
print(most_recent_song(data))
print(count_plays(data))
print(most_played_artists(data))