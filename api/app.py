from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from slackeventsapi import SlackEventAdapter
import os

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

# Set up listener for slack stuff
SLACK_SIGNING_SECRET=os.environ.get("SLACK_SIGNING_SECRET")
# Bind the Events API route to your existing Flask app by passing the server
# instance as the last param, or with `server=app`.
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)

# Create an event listener for "reaction_added" events and print the emoji name
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
  emoji = event_data["event"]["reaction"]
  print(emoji)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
