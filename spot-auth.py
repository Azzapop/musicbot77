import os
from sys import argv
from bottle import route, run, request
import spotipy
from spotipy import oauth2
from multiprocessing import Pool

SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI')
CACHE = '.cache'
# 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private streaming user-follow-modify user-follow-read user-library-read user-library-modify user-read-private user-read-birthdate user-read-email user-top-read user-modify-playback-state'

SCOPE = 'user-library-read user-modify-playback-state'
sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE)
sp = None

def handle_command(command, channel):
    response = 'ba dum tsss'
    if command.startswith(EXAMPLECOMMAND):
        if sp:
            tracks = sp.current_user_saved_tracks()
            response = tracks
        else:
            response = 'Looks like youre not authd: go to this link to auth:' + sp_oauth.get_authorize_url()
    slack_client.api_call('chat.postMessage', channel=channel, text=response, as_user=True)

def parse_slack_output(output):
    if output and len(output) > 0:
        for o in output:
            if o and 'text' in o and ATBOT in o['text']:
                return o['text'].split(ATBOT)[1].strip().lower(), o['channel']
    return None, None

def bot():
    DELAY = 1
    if slack_client.rtm_connect():
        print('made it!')
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")


pool = Pool(processes=1)
pool.apply_async(bot)

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
