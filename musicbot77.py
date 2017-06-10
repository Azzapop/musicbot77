import os
import time
from slackclient import SlackClient

BOTID = os.environ.get('BOTID')
ATBOT = "<@"+BOTID+">"
EXAMPLECOMMAND = "do"

slack_client = SlackClient(os.environ.get('MUSICBOT77'))

def handle_command(command, channel):
    response = 'test'
    if command.startswith(EXAMPLECOMMAND):
        response = 'thats the example command'
    slack_client.api_call('chat.postMessage', channel=channel, text=response, as_user=True)

def parse_slack_output(output):
    if output and len(output) > 0:
        for o in output:
            if o and 'text' in o and ATBOT in o['text']:
                print('here')
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
