import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

CLIENT_ID = 'IDValue'
CLIENT_SECRET = 'SecretValue'
REDIRECT_URI = 'URIValue'

SCOPE = 'playlist-read-private'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def export_playlist_to_csv(playlist_id, csv_filename):
    tracks = get_playlist_tracks(playlist_id)
    track_list = []
    
    for item in tracks:
        track = item['track']
        track_list.append({
            'Track Name': track['name'],
            'Artist': ', '.join([artist['name'] for artist in track['artists']]),
        })
    
    df = pd.DataFrame(track_list)
    df.to_csv(csv_filename, index=False)
    print(f'Playlist exported to {csv_filename}')

playlist_id = '5KbW3oX6d1FfHYWzyxwqGD'  # Replace with your playlist ID
csv_filename = 'nostalgia.csv'
export_playlist_to_csv(playlist_id, csv_filename)
