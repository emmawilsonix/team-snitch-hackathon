from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from routes.users import users_routes
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DBHOST", "mysql://root:lolviper@localhost/Hogwarts")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.register_blueprint(users_routes)
db = SQLAlchemy(app)

@app.route("/")
def home():
    return "Welcome to Hogwarts 🧙"

@app.route('/test')
def testdb():
    # lmao get rekt
    try:
        db.session.query("1").from_statement(text("SELECT 1")).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        print(e)
        return '<h1>Something is broken.</h1>'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
