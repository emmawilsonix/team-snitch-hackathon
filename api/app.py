import random
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from routes.users import users_routes
from routes.home import home_routes
from flask_cors import CORS
from mocks import mock_user_list, mock_teams_list, mock_team_with_users
from slackeventsapi import SlackEventAdapter
import os
from slack_sdk import WebClient

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DBHOST", "mysql://root:lolviper@localhost/Hogwarts")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.register_blueprint(users_routes)
app.register_blueprint(home_routes)
CORS(app)
db = SQLAlchemy(app)

@app.route('/test/users', methods=['GET'])
def testusersget():
    if request.args.get('teamID'):
        arg = request.args.get('teamID')
        if arg:
            users = []
            for d in mock_user_list:
                if int(d['teamID']) == int(arg):
                    users.append(d)
            return jsonify(users)
    return jsonify(mock_user_list)

@app.route('/test/teams', methods=['GET'])
def testteamsget():
    for team in mock_teams_list:
        team['team_points'] = random.randint(1, 8772274669)
    return jsonify(mock_teams_list)

@app.route('/test/teams/<id>', methods=['GET'])
def testteamsgetbyid(id):
    for d in mock_team_with_users:
        if int(d['teamID']) == int(request.view_args['id']):
            return jsonify(d)


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
    slack_message, msg, mentioned_user = "", "", None
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
                msg = "Hey <@" + mentioned_user["user"]["id"] + "> you got " + str(points) + " points from <@" + source_user["user"]["id"] + ">!"
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

class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    teamID = db.Column(db.Integer, db.ForeignKey('teams.teamID'))
    emailAddress = db.Column(db.String(255))

@app.route('/users', methods=['GET', 'POST'])
def users_list():
    if request.method == 'GET':
        if request.query_string:
            if (
                request.args.get('teamID') is None and 
                request.args.get('orderby') is None
            ):
                return "Bad request param", 400
            if request.args.get('teamID'):
                # do team ID select
                pass
            if request.args.get('orderby'):
                # do orderby select
                pass
        else:
            # select entire users list
            pass
    elif request.method == 'POST':
        # create the user breh
        pass

    else:
        return "Bad request method breh", 405


    return "users brah"

    