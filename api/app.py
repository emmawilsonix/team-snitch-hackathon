import random
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from sqlalchemy.sql import text
from routes.home import home_routes
from flask_cors import CORS
from mocks import mock_user_list, mock_teams_list, mock_team_with_users
from slackeventsapi import SlackEventAdapter
import os
import random
from slack_sdk import WebClient

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DBHOST", "mysql://root:lolviper@localhost/Hogwarts")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.register_blueprint(home_routes)
CORS(app)
db = SQLAlchemy(app)
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST", "us-cdbr-east-02.cleardb.com")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER", "b624ad11003645")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD", "viper67") #this one is fake
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB", "heroku_59a59d73fbb7df4")

mysql = MySQL(app)

# todo: Pull these from the db
TEAM_IDS=[189651,189641,189631,189661]
TEAM_NAME={189651: "Coffee Cat",189641: "Dancing Banana",189631: "Party Parrot",189661: "Yay Orange"}

# Bind the Events API route to your existing Flask app
SLACK_SIGNING_SECRET=os.environ.get("SLACK_SIGNING_SECRET")
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)

# Create a SlackClient for your bot to use for Web API requests
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
slack_client = WebClient(token=SLACK_BOT_TOKEN)

SLACKBOT_USERID="U01F944MG3X"
GENERAL_CHANNEL="C01FJ6SBZQU"
TEST_CHANNEL="C01FF40BAPL"

class Users(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    teamID = db.Column(db.Integer, db.ForeignKey('teams.teamID'))
    emailAddress = db.Column(db.String(255))
    def serialize(self):
        image_url = "../../assets/images/unknown.png"
        try: 
            user_info = slack_client.users_lookupByEmail(email=emailAddress)
            image_url = user_info["user"]["profile"]["image_72"]
        except:
            print("oops couldn't get an image for the user")
        return {"userID": self.userID,
                "teamID": self.teamID,
                "emailAddress": self.emailAddress,
                "img": my_image_url}

class Teams(db.Model):
    teamID = db.Column(db.Integer, primary_key=True)
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
                user = Users.query.filter_by(teamID=int(request.args.get('teamID')))
                return jsonify(user.first().serialize()) if user.first() else {}
        else:
            users = Users.query.all()
            return jsonify([user.serialize() for user in users])
    elif request.method == 'POST':
        data = request.json
        user = Users(teamID=data.get('teamID'), emailAddress=data.get('emailAddress'))
        db.session.add(user)
        db.session.commit()

        return jsonify(user.serialize())
    else:
        return "Bad request method breh", 405


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
                #React to the slack post now, for some sense of transparency
                slack_client.reactions_add(channel=message["channel"], timestamp=message["event_ts"], name="thumbsup")
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
    try:
        query="""INSERT INTO points (userid, sourceUserID, points) VALUES ((SELECT userID FROM users WHERE emailAddress = %s), (SELECT userID FROM users WHERE emailAddress = %s), %s)"""
        cur = mysql.connection.cursor()
        cur.execute(query, (source_user_email, mentioned_user_email, points))
        mysql.connection.commit()
        cur.close()
        return None
    except:
        return "Something something database?"

# Create an event listener for users joining the #general channel
@slack_events_adapter.on("member_joined_channel")
def handle_user_joined_channel(event_data):
    message = event_data["event"]

    # Only create accounts when certain channels are joined.
    if message["channel"] != TEST_CHANNEL and message["channel"] != GENERAL_CHANNEL:
        print("member joined a channel we don't care about...")
        return

    # Get user info and add them to the DB.
    joined=message["user"]
    joined_user = slack_client.users_info(user=joined)
    joined_user_email = joined_user["user"]["profile"]["email"]
    team = try_add_user(joined_user_email)
    if team is None:
        msg = """Hey <@{joined}> :wave: I'm <@{snitch}>! Looks like you joined #general but something went wrong so I wasn't able to assign you a team. 

Either you already have a house (congrats!) or you should try leaving/re-joining #general.

Much Love :heart: <@snitch>""".format(joined=joined, snitch=SLACKBOT_USERID)
    else:

        msg = """Hey <@{joined}> :wave: I'm <@{snitch}>!

<@{snitch}> is a Harry Potter inspired slack bot designed to encourage and celebrate Little Big Wins by giving house points to your fellow IXers.

You'll be sorted into a team and you can win points for your team by showing off your IX class! 

You can award points to other IXers by @ mentioning me and someone you want to give points to on slack! Just tell me how many points to give them and I am on it! 

Looks like you've been sorted into *{team}*! Congratulations that's one of the best ones.

⚡ Make sure to check out the leaderboard <https://snitch-leaderboard.herokuapp.com/|here>! ⚡

⚡ And get to snitching! ⚡

Much Love :heart: <@snitch>""".format(joined=joined, snitch=SLACKBOT_USERID, team=team)

    print("Sending %s the following alert: %s" %(joined, msg))
    slack_client.chat_postMessage(channel=joined, text=msg)

def try_add_user(user_email):
    """
    try_add_user tries to add a user to the db. 
        @user_email = the e-mail of the user being added
    function returns the house the user belongs to. 
    Return None if the user cannot be created.
    If the user already exists return their team.
    """

    query="""INSERT INTO users (teamID, emailAddress) VALUES (%s, %s)"""
    print(query)
    team_assign=random.choice(TEAM_IDS)
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (team_assign, user_email))
        mysql.connection.commit()
        cur.close()
        return TEAM_NAME[team_assign]
    except:
        return None


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)