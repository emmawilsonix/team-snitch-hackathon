import random
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from routes.users import users_routes
from routes.home import home_routes
from flask_cors import CORS
from mocks import mock_user_list, mock_teams_list, mock_team_with_users
import os

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


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
