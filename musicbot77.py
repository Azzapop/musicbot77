import os
import time
from slackclient import SlackClient

BOTID = os.environ.get('BOTID')
ATBOT = "<@"+BOTID+">"
EXAMPLECOMMAND = "do"

slack_client = SlackClient(os.environ.get('MUSICBOT77'))

import spotipy
from spotipy import oauth2

SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECRT_URI = os.environ.get('SPOTIPY_REDIRECT_URI')
CACHE = '.cache'

# 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private streaming user-follow-modify user-follow-read user-library-read user-library-modify user-read-private user-read-birthdate user-read-email user-top-read user-modify-playback-state'

SCOPE = 'user-library-read user-modify-playback-state'
sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE)


def spotify_auth():
    access_token = ''
    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Got token info!")
        access_token = token_info['access_token']
    if access_token:
        print("Access token available! Attempting to get user information.")
        return True, spotipy.Spotify(access_token)
    else:
        return False, sp_oauth.get_authorize_url()

def handle_command(command, channel):
    authd, sp = spotify_auth()
    response = 'ba dum tsss'
    if command.startswith(EXAMPLECOMMAND):
        if authd:
            tracks = sp.current_user_saved_tracks()
            response = tracks
        else:
            response = 'Looks like youre not authd: go to this link to auth:' + sp
    slack_client.api_call('chat.postMessage', channel=channel, text=response, as_user=True)

def parse_slack_output(output):
    if output and len(output) > 0:
        for o in output:
            if o and 'text' in o and ATBOT in o['text']:
                return o['text'].split(ATBOT)[1].strip().lower(), o['channel']
    return None, None

if __name__ == "__main__":
    DELAY = 1
    if slack_client.rtm_connect():
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
