from flask_sqlalchemy import SQLAlchemy
from app import db

class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True, nullable=False)
    teamID = db.Column(db.Integer, db.ForeignKey('teams.teamID'), nullable=False)
    emailAddress = db.Column(db.String(100), nullable=False)

class Point(db.Model):
    date = db.Column(db.DateTime, primary_key=True, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), primary_key=True, nullable=False)
    sourceUserID = db.Column(db.Integer, db.ForeignKey('users.userID'), primary_key=True, nullable=False)
    points = db.Column(db.Integer, nullable=False)