# app.py
import sqlite3
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
import validator
import recommendor
import login
#import UserInfo from './userinfo'

app = Flask(__name__)
CORS(app)

@app.route('/login/', methods=['POST'])
def log_in():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    if not request.form:
        app.logger.warning(f"Welcome back, {username}!")
    app.logger.warning(f"received username {username}, password {password}, entirepayload {request.form}")
    valid_cred, error = validator.validate_login(username, password)
    response = {}
    if valid_cred:
        response["MESSAGE"] = f"Welcome {username} to our app!"
    else:
        response["ERROR"] = error[0]
    #
    return jsonify(response)

@app.route('/signup/', methods=['POST'])
def signin():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    app.logger.warning(f"received username {username}, password {password}, entirepayload {request.form}")
    valid_cred, error = validator.validate_login(username, password)
    response = {}
    if valid_cred:
        login.create_user()
        response["MESSAGE"] = f"Welcome " #여기에 user id printing
    else:
        response["ERROR"] = error[0]
    #
    return jsonify(response)

'''@app.route('/get/', methods=['GET'])
def generate_session_id():
    session_id = str(uuid.uuid4())
    param = request.form.get('username')
    return session_id'''

@app.route('/restaurants/', methods=['GET'])
def get_restaurants():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    restaurants = recommendor.get_recommended_restaurants(lat, lon)
    return restaurants

# A welcome message to test our server
@app.route('/')
def index():
    login()
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
