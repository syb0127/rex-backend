# app.py
import sqlite3
import uuid
from flask import Flask, request, jsonify
from flask.logging import create_logger
from flask_cors import CORS
import validator
import recommendor
import login
#import UserInfo from './userinfo'

app = Flask(__name__)
CORS(app)
logger = create_logger(app)

@app.route('/login/', methods=['POST'])
def log_in():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    if not request.form:
        logger.warning(f"Welcome back, {username}!")
    logger.warning(f"received username {username}, password {password}, entirepayload {request.form}")
    valid_cred, error = validator.validate_login(username, password)
    response = {}
    if valid_cred:
        response["MESSAGE"] = f"Welcome back, {username}!"
    else:
        response["ERROR"] = error[0]
    #
    return jsonify(response)

@app.route('/signup/', methods=['POST'])
def signup():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    email = request.form.get("email", None)
    logger.warning(f"received username {username}, password {password}, entirepayload {request.form}")
    valid_cred, error = validator.validate_signup(username, password, email)
    response = {}
    if valid_cred:
        login.create_user(username, password, email)
        response["MESSAGE"] = f"Welcome {username} to our app!" #여기에 user id printing
    else:
        response["ERROR"] = error[0]
    #
    return jsonify(response)

'''@app.route('/get/', methods=['GET'])
def generate_session_id():
    session_id = str(uuid.uuid4())
    param = request.form.get('username')
    return session_id'''

@app.route('/restaurant/', methods=['GET'])
def get_restaurants():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    restaurants = recommendor.get_recommended_restaurants(lat, lon)
    return restaurants

@app.route('/restaurant/feedback/', methods=['POST'])
def save_restaurant_feedback():
    place_id = request.form.get("place_id")
    feedback = request.form.get("feedback")
    successfully_updated = recommendor.adjust_personal_restaurant_rating(place_id, feedback)
    return successfully_updated

# A welcome message to test our server
@app.route('/')
def index():
    
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
