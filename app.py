# app.py
from flask import Flask, request, jsonify
from validator import validate_login
from flask_cors import CORS
from flask.logging import create_logger
import sqlite3
import uuid
#import UserInfo from './userinfo'

app = Flask(__name__)
create_logger(app)

@app.route('/login/', methods=['POST'])
def login():
    if not request.form:
        app.logger.error(f"could not parse a request: {request.data}")
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    app.logger.warning(f"received username {username}, password {password}, entirepayload {request.form}")
    valid_cred, error = validate_login(username, password)
    response = {}
    if valid_cred:
        response["MESSAGE"] = f"Welcome {username} to our app!"
    else:
        response["ERROR"] = error[0]
    return jsonify(response)

@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name', None)
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {param} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

@app.route('/get/', methods=['GET'])
def generate_session_id():
    session_id = str(uuid.uuid4())
    param = request.form.get('username')
    return session_id

@app.route('/post/', methods=['POST'])
def post_restaurants():
    return

@app.route('/get/', methods=['GET'])
def get_restaurants():
    return

# A welcome message to test our server
@app.route('/')
def index():
    login()
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
