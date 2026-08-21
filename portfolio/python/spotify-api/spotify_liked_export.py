import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

CLIENT_ID = 'IDValue'
CLIENT_SECRET = 'SecretValue'
REDIRECT_URI = 'URIValue'

SCOPE = 'user-library-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

def fetch_liked_songs(sp):
    liked_songs = []
    results = sp.current_user_saved_tracks(limit=50)
    while results:
        for item in results['items']:
            track = item['track']
            liked_songs.append({
                'name': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']])
            })
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return liked_songs

liked_songs = fetch_liked_songs(sp)

df = pd.DataFrame(liked_songs)

df.to_csv('liked_songs.csv', index=False)

print('Exported songs to liked_songs.csv in current directory')
