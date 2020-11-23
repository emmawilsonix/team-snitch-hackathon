from flask import Flask
import os
import threading
import time
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)

# This should be run in the terminal: 
# export SLACK_BOT_TOKEN='xoxb-1522067689266-1519140730133-eufROWvsyLgZWMltdL7NUwDR'
SLACK_SIGNING_SECRET = '9abe82c0eb94caca58b43957653142d6'
SLACK_BOT_TOKEN="xoxb-1522067689266-1519140730133-eufROWvsyLgZWMltdL7NUwDR"
BOT_NAME = "HogBot"

slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, endpoint="/slack/events")

# Create an event listener for "reaction_added" events and print the emoji name
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
  emoji = event_data["event"]["reaction"]
  print(emoji)

@app.route("/")
def home():
    return "Welcome to Hogwarts"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)