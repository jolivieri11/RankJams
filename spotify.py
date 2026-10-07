import base64
import time

import requests

from config import Settings

def _get_bearer_token() -> dict:
    token_url = 'https://accounts.spotify.com/api/token'
    token_headers = {
        'Authorization': 'Basic ' + base64.b64encode((Settings.SPOTIFY_CLIENT_ID + ':' + Settings.SPOTIFY_CLIENT_SECRET).encode()).decode()
    }
    response = requests.post(token_url, headers=token_headers, data={'grant_type': 'client_credentials'}, timeout=10)
    response.raise_for_status()
    json_response = response.json()
    return {"token": json_response.get('access_token'), "expires_at": time.time() + json_response.get('expires_in')}

def id_to_song(song_id: str, bearer: dict) -> dict:
    access_token = bearer.get("token")
    if bearer.get("expires_at") - 60 < time.time():
        bearer.update(_get_bearer_token())
        access_token = bearer.get("token")
    song_url = f'https://api.spotify.com/v1/tracks/{song_id}'
    song_headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(song_url, headers=song_headers, timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    song_link = input("Input a valid spotify track link: ")
    track_data = id_to_song(song_link.split('/')[-1], _get_bearer_token())
    print(f"{track_data.get('name')} - {track_data.get('artists')[0].get('name')}")