from flask import Blueprint, request

users_routes = Blueprint('users_routes', __name__, template_folder='templates')
@users_routes.route('/users', methods=['GET', 'POST'])
def users_list():
    return "users brah"

    