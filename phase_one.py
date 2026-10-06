import base64
import requests
import time

from config import Settings

def _get_bearer_token() -> dict:
    token_url = 'https://accounts.spotify.com/api/token'
    token_headers = {
        'Authorization': 'Basic ' + base64.b64encode((Settings.SPOTIFY_CLIENT_ID + ':' + Settings.SPOTIFY_CLIENT_SECRET).encode()).decode()
    }
    try:
        response = requests.post(token_url, headers=token_headers, data={'grant_type': 'client_credentials'}, timeout=10)

        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error obtaining bearer token: {e}")
        return {"token": None, "expires_in": 0}
    except requests.exceptions.RequestException as e:
        print(f"Error obtaining bearer token: {e}")
        return {"token": None, "expires_in": 0}
    return {"token": response.json().get('access_token'), "expires_at": time.time() + response.json().get('expires_in')}

def id_to_song(song_id: str, bearer: dict) -> dict:
    access_token = bearer.get("token")
    if not access_token:
        print("Failed to obtain access token.")
        return {}
    song_url = f'https://api.spotify.com/v1/tracks/{song_id}'
    if bearer.get("expires_at") - 60 < time.time():
            bearer = _get_bearer_token()
            access_token = bearer.get("token")
    song_headers = {
        'Authorization': 'Bearer ' + access_token
    }
    try:
        response = requests.get(song_url, headers=song_headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error obtaining song data: {e}")
        return {}
    except requests.exceptions.RequestException as e:
        print(f"Error obtaining song data: {e}")
        return {}
    return response.json()

track_data = id_to_song('3adRTDxuj3yPDhRJs1PF2C', _get_bearer_token())
print(f"{track_data.get('name')} - {track_data.get('artists')[0].get('name')}")