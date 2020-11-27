import random
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
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
app.config['SQLALCHEMY_POOL_RECYCLE'] = 28800 - 1
app.register_blueprint(home_routes)
CORS(app)
db = SQLAlchemy(app)

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

# Locally cache profile pictures because slack seems to be rate limiting us.
profile_pic_cache = {}

class Users(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    teamID = db.Column(db.Integer, db.ForeignKey('teams.teamID'))
    emailAddress = db.Column(db.String(255))
    name = db.Column(db.String(255))
    def serialize(self):
        image_url = "../../assets/images/unknown.png"
        try: 
            if self.emailAddress in profile_pic_cache:
                image_url = profile_pic_cache[self.emailAddress]
            else:
                user_info = slack_client.users_lookupByEmail(email=self.emailAddress)
                image_url = user_info["user"]["profile"]["image_72"]
                profile_pic_cache[self.emailAddress] = image_url
        except:
            print("oops couldn't get an image for the user")
        return {"userID": self.userID,
                "teamID": self.teamID,
                "name": self.name,
                "img": image_url}

class Teams(db.Model):
    teamID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    def serialize(self):
        return {
                "teamID": self.teamID,
                "name": self.name
            }


class Points(db.Model):
    date = db.Column(db.String(255), primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), primary_key=True)
    sourceUserID = db.Column(db.Integer, db.ForeignKey('users.userID'), primary_key=True)
    points = db.Column(db.Integer)
    def serialize(self):
        return {"points": self.points}
      
# #########################################################
# ############# front-end api routes !!!! #################
# #########################################################

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
            response = [user.serialize() for user in users]
            for user in response:
                points = Points.query.filter_by(userID=user.get("userID")).all()
                total_points = 0
                for p in points:
                    total_points += p.serialize().get('points')
                user['points'] = total_points
            return jsonify(response)
    elif request.method == 'POST':
        data = request.json
        user = Users(teamID=data.get('teamID'), emailAddress=data.get('emailAddress'))
        db.session.add(user)
        db.session.commit()

        return jsonify(user.serialize())
    else:
        return "Bad request method breh", 405

@app.route('/teams', methods=['GET'])
def teams_list():
    if request.method == 'GET':
        teams = [team.serialize() for team in Teams.query.all()]
        for t in teams:
            users = Users.query.filter_by(teamID=t['teamID'])
            team_points = 0
            for user in users:
                points = Points.query.filter_by(userID=user.serialize().get("userID")).all()
                for p in points:
                    team_points += p.serialize().get('points')
            t['team_points'] = team_points
        
        return jsonify(teams)

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

# #########################################################
# ############ slack listener routes !!!! #################
# #########################################################

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
            original_message = slack_client.chat_getPermalink(channel=message["channel"], message_ts=message["ts"])
            # Try to grant points
            if points > 10:
                msg = """Hey <@{source}> :wave: I couldn't do <{permalink}|this>. 
                
You can give a maximum of 10 points at a time! You should try giving <@{mentioned}> some points again (but only up to 10, remember?)!""".format(source=source_user["user"]["id"], permalink=original_message["permalink"], mentioned=mentioned_user["user"]["id"])
            else:
                error = try_grant_points(source_user_email, mentioned_user_email, points)
                if error is None:
                    msg = """Hey <@{mentioned}> :wave: <{permalink}|you got {points} points> from <@{source}>!

    ⚡ Check out the leaderboard <https://snitch-leaderboard.herokuapp.com/|here>! ⚡

    ⚡ And get to snitching! ⚡""".format(mentioned=mentioned_user["user"]["id"], points=str(points), source=source_user["user"]["id"], permalink=original_message["permalink"])
                    notify_user = mentioned_user["user"]["id"]
                    #React to the slack post now, for some sense of transparency
                    try:
                        slack_client.reactions_add(channel=message["channel"], timestamp=message["event_ts"], name="thumbsup")
                    except:
                        print("well that's too bad I couldn't react... try again with another emoji")
                        try:
                            slack_client.reactions_add(channel=message["channel"], timestamp=message["event_ts"], name="white_check_mark")
                        except: 
                            print("something went really really wrong")
                            pass
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
        to_user_id = Users.query.filter_by(email_address=mentioned_user_email).first().serialize()['userID']
        from_user_id = Users.query.filter_by(email_address=source_user_email).first().serialize()['userID']
        inserted_points = Points(userID=to_user_id, sourceUserID=from_user_id, points=points)
        db.session.add(inserted_points)
        db.session.commit()
        return None
    except Exception as e:
        return e

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
    joined_user_name = joined_user["user"]["profile"]["real_name_normalized"]
    team = try_add_user(joined_user_email, joined_user_name)
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

def try_add_user(user_email, user_name):
    """
    try_add_user tries to add a user to the db. 
        @user_email = the e-mail of the user being added
    function returns the house the user belongs to. 
    Return None if the user cannot be created.
    If the user already exists return their team.
    """

    query="""INSERT INTO users (teamID, emailAddress, name) VALUES (%s, %s, %s)"""
    print(query)
    team_assign=random.choice(TEAM_IDS)
    try:
        user = Users(teamID=team_assign, emailAddress=user_email, name=user_name)
        db.session.add(user)
        db.session.commit()
        return TEAM_NAME[team_assign]
    except Exception as e:
        return e


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)