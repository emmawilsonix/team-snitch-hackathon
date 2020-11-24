from flask_sqlalchemy import SQLAlchemy
from database.database import db

class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    teamID = db.Column(db.Integer, db.ForeignKey('teams.teamID'))
    emailAddress = db.Column(db.String(255))