import os
from slackclient import SlackClient

BOT_NAME = 'musicbot77'

slack_client = SlackClient(os.environ.get('MUSICBOT77'))

if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
