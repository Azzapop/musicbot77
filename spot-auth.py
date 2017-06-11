import os
from sys import argv
from bottle import route, run, request
import spotipy
from spotipy import oauth2

SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECRT_URI = os.environ.get('SPOTIPY_REDIRECT_URI')
CACHE = '.cache'

# 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private streaming user-follow-modify user-follow-read user-library-read user-library-modify user-read-private user-read-birthdate user-read-email user-top-read user-modify-playback-state'

SCOPE = 'user-library-read user-modify-playback-state'
sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE)

@route('/')
def index():
    access_token = ''
    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Got token info!")
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            print("Found auth code! Attempting to get access token.")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print("Access token available! Attempting to get user information.")
        sp = spotipy.Spotify(access_token)
        tracks = sp.current_user_saved_tracks()
        return tracks
    else:
        return htmlLoginButton

def htmlForLoginButton():
    auth_url = sp_oauth.get_authorize_url()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton

run(host='0.0.0.0', port=argv[1])
