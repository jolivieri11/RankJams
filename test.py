import json

# Loads listening data
def load_json(file_path) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)

# Returns the data sorted by most recent plays
def sort_data_by_recent(data: dict) -> dict:
    new_data = {}
    new_data['items'] = sorted(data.get('items', []), key=lambda item: item['played_at'], reverse=True)
    return new_data

def print_play_history(data: dict) -> None:
    for item in data.get('items', []):
        print(f"{item['track']['name']} - {', '.join(artist['name'] for artist in item['track']['artists'])} (Played at: {item['played_at']})")

# Returns dictionary of song plays sorted by play count in descending order
def print_count_plays(data: dict) -> dict:
    plays = {}
    names = {}  # Maps song_id to song name
    if not data:
        return plays
    for item in data.get('items', []):
        song_id = item['track']['id']
        plays[song_id] = plays.get(song_id, 0) + 1
        names[song_id] = f"{item['track']['name']} - {', '.join(artist['name'] for artist in item['track']['artists'])}"
    for item, play_count in sorted(plays.items(), key=lambda item: item[1], reverse=True):
        print(f"{names[item]} | Plays: {play_count}")
    return plays
    
# Returns the top 5 most played artists
def most_played_artists(data: dict) -> dict:
    artists = {}
    if not data.get('items'):
        return artists
    for item in data['items']:
        for artist in item['track']['artists']:
            artist_name = artist['name']
            artists[artist_name] = artists.get(artist_name, 0) + 1
    return dict(sorted(artists.items(), key=lambda item: item[1], reverse=True)[:5])

if __name__ == "__main__":
    data = load_json('listening_history.json')
    data = sort_data_by_recent(data)
    print_play_history(data)
    print("-"*10)
    print_count_plays(data)
    print("-"*10)
    print(most_played_artists(data))