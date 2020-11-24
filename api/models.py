from flask_sqlalchemy import SQLAlchemy
from app import db

class Team(db.Model):
    teamID = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)

class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True, nullable=False)
    teamID = db.Column(db.Integer, db.ForeignKey('teams.teamID'), nullable=False)
    emailAddress = db.Column(db.String(100), unique=True, nullable=False)
