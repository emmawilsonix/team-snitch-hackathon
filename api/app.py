from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from slackeventsapi import SlackEventAdapter
import os
from slack_sdk import WebClient

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DBHOST", "mysql://root:lolviper@localhost/Hogwarts")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

@app.route("/")
def home():
    return "Welcome to Hogwarts 🧙"

@app.route('/test')
def testdb():
    try:
        db.session.query("1").from_statement(text("SELECT 1")).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        print(e)
        return '<h1>Something is broken.</h1>'

# Bind the Events API route to your existing Flask app
SLACK_SIGNING_SECRET=os.environ.get("SLACK_SIGNING_SECRET")
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)

# Create a SlackClient for your bot to use for Web API requests
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
slack_client = WebClient(token=SLACK_BOT_TOKEN)

SLACKBOT_USERID="U01F944MG3X"

# Create an event listener for @bot mentions
@slack_events_adapter.on("app_mention")
def handle_app_mention(event_data):
    message = event_data["event"]

    # Get the user who initiated the @mention
    source_user = slack_client.users_info(user=message["user"])

    # Iterate through message body looking for the destination user. Use the first match.
    elements = message["blocks"][0]["elements"][0]["elements"]
    mentioned_user = None
    slack_message = ""
    notify_user = ""
    for element in elements:
        if element["type"] == "user" and element["user_id"] != SLACKBOT_USERID:
            mentioned_user = slack_client.users_info(user=element["user_id"])
            break
    if mentioned_user is not None:
        source_user_email = source_user["user"]["profile"]["email"]
        mentioned_user_email = mentioned_user["user"]["profile"]["email"]
        if try_grant_points(source_user_email, mentioned_user_email):
            print(source_user_email + " granted a point to " + mentioned_user_email + "...")
            slack_message = "Hey <@" + mentioned_user["user"]["id"] + "> you got a point from <@" + source_user["user"]["id"] + ">!"
            notify_user = mentioned_user["user"]["id"]
        else:
            print(source_user_email + " failed to give a point to " + mentioned_user_email + "...")
            slack_message = "Hey <@" + source_user["user"]["id"] + "> - I couldn't give <@" + mentioned_user["user"]["id"] + "> a point... can you try again?"
            notify_user = source_user["user"]["id"]
    else:
        slack_message = "Hey <@" + source_user["user"]["id"] + "> something funny just happened... can you try granting that point again?"
        notify_user = source_user["user"]["id"]
        print("Unable to grant points...")

    slack_client.chat_postMessage(channel=notify_user, text=slack_message)


def try_grant_points(source_user_email, mentioned_user_email):
    return True



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
