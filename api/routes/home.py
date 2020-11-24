from flask import Blueprint, request

home_routes = Blueprint('home_routes', __name__)
@home_routes.route('/')
def home():
    return "Welcome to Hogwarts 🧙"
