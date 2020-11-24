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

    # Default variable values
    slack_message, msg, mentioned_user, attachments = "", "", None, None
    notify_user = source_user["user"]["id"]
    
    # Iterate through message body looking for the destination user. Use the first match.
    elements = message["blocks"][0]["elements"][0]["elements"]
    for element in elements:
        if element["type"] == "user" and element["user_id"] != SLACKBOT_USERID:
            mentioned_user = slack_client.users_info(user=element["user_id"])
            break

    # If there was a user mention, handle the points.
    if mentioned_user is not None:
        if source_user["user"]["id"] == mentioned_user["user"]["id"]:
            msg = "Hey <@" + source_user["user"]["id"] + "> - nice try but you can only give points to others"
        else:
            # Try to get the number of points, default to 1.
            text = message.get('text')
            points_array = [int(s) for s in text.split() if s.isdigit()]
            points = 1 if len(points_array) == 0 else points_array[0]

            source_user_email = source_user["user"]["profile"]["email"]
            mentioned_user_email = mentioned_user["user"]["profile"]["email"]
            # Try to grant points
            error = try_grant_points(source_user_email, mentioned_user_email, points)
            if error is None:
                original_message = slack_client.chat_getPermalink(channel=message["channel"], message_ts=message["ts"])
                msg = """Hey <@{mentioned}> :wave: <{permalink}|you got {points} points> from <@{source}>!

⚡ Check out the leaderboard <https://snitch-leaderboard.herokuapp.com/|here>! ⚡

⚡ And get to snitching! ⚡""".format(mentioned=mentioned_user["user"]["id"], points=str(points), source=source_user["user"]["id"], permalink=original_message["permalink"])
                notify_user = mentioned_user["user"]["id"]
            # If we couldn't grant points, let people know
            else:
                msg = "Hey <@" + source_user["user"]["id"] + "> - I couldn't give <@" + mentioned_user["user"]["id"] + "> points from you, here's what the computer told me: " + error
    # If there was no user mention, handle the error.
    else:
        msg = "Hey <@" + source_user["user"]["id"] + "> something funny just happened... can you try granting that point again?"

    print("Sending %s the following alert: %s" %(notify_user, msg))
    slack_client.chat_postMessage(channel=notify_user, text=msg)

def try_grant_points(source_user_email, mentioned_user_email, points):
    """
    try_grant_points tries to grant points to a user. 
        @source_user_email = the user granting the points
        @mentioned_user_email = the user getting the points
        @points = an int representing the number of points being granted
    function returns None if no errors occur during execution, and a string representing the error if an error does occur.
    """
    return None



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
