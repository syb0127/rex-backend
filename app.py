# app.py
import sqlite3
import uuid
from flask import Flask, request, jsonify
from flask.logging import create_logger
from flask_cors import CORS
import validator
import recommendor
import login

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
    status_code = 200
    if valid_cred:
        session_token = login.get_session_token(username, password)
        if session_token is None:
            response["error"] = f"Given username and password do not exist."
            status_code = 403
        else:
            response["session_token"] = session_token
    else:
        response["error"] = error[0]
        status_code = 403
    return response, status_code

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
        response["message"] = f"Welcome {username} to our app!" 
    else:
        response["error"] = error[0]
    return jsonify(response)

@app.route('/restaurant/', methods=['GET'])
def get_restaurants():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    logger.warning(f"lat {lat}, lon {lon}")
    restaurants = recommendor.get_recommended_restaurants(lat, lon)
    return {"results": restaurants}

@app.route('/restaurant/feedback/', methods=['POST'])
def save_restaurant_feedback():
    session_token = request.headers.get("session_token")
    place_id = request.form.get("place_id")
    feedback = request.form.get("feedback")
    if session_token is None or not session_token:
        return {'error': "Did not receive `session_token`"}, 400
    user_id = login.get_user_id_by_session_token(session_token)
    if user_id is None:
        return {'error': "Session does not exist."}, 403
    successfully_updated = recommendor.adjust_personal_restaurant_rating(user_id, place_id, feedback)
    if not successfully_updated:
        return {'error': "Failed to update rating"}, 500
    return {'message': "Success"}, 200

# A welcome message to test our server
@app.route('/')
def index():
    
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
