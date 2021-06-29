import sqlite3 
from flask import current_app
'''from werkzeug.debug import get_current_traceback

import sentry_sdk

sentry_sdk.init(
    "https://examplePublicKey@o0.ingest.sentry.io/0",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)'''
def initialize_db():
    connection = sqlite3.connect('userinfo.db')

    # create a cursor
    c = connection.cursor()

    # create a table
    # Username text,
    c.execute("""CREATE TABLE user (
            user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(20) NOT NULL UNIQUE,
            salted_password VARCHAR(30) NOT NULL,
            email VARCHAR(50) NOT NULL UNIQUE
        )""")
    c.execute("""CREATE TABLE rating (
            rating_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            place_id VARCHAR(30) NOT NULL,
            rating_score INTEGER NOT NULL
        )""")

    connection.commit()
    connection.close()

#주어진 디비를 읽고 쓰는 역할을 함

def get_user_id(username, pwd_salted_hash):
    if username == "apple":
        if pwd_salted_hash == '2fc732c99952d54e197ee42a2c0ff3ae66a225f8':
            return 1
        else:
            return -1
    else:
        return -1

def is_username_duplicate(username):
    """checks if username already exists and returns boolean
        if db connection fails, return None"""
    connection = sqlite3.connect('userinfo.db')
    # create a cursor
    c = connection.cursor()
    try:
        c.execute(f"SELECT COUNT(*) FROM user WHERE user.username = ?", (username,))
        connection.commit()
        return c.fetchone()[0] > 0
    except Exception as e:
        #current_app.logger.error(f"Failed to count (username {username}) from `user` table: {e}")
        print(f"Failed to count (username {username}) from `user` table: {e}")
        return None

def is_email_duplicate(email):
    """checks if email already exists and returns boolean
        if db connection fails, return None"""
    connection = sqlite3.connect('userinfo.db')
    # create a cursor
    c = connection.cursor()
    try:
        c.execute(f"SELECT COUNT(*) FROM user WHERE user.email = ?", (email,))
        connection.commit()
        return c.fetchone()[0] > 0
    except Exception as e:
        #current_app.logger.error(f"Failed to count (email {email}) from `user` table: {e}")
        print(f"Failed to count (email {email}) from `user` table: {e}")
        return None

def insert_new_user(username, pwd_salted_hash, email):
    connection = sqlite3.connect('userinfo.db')
    # create a cursor
    c = connection.cursor()
    try:
        c.execute(f"INSERT INTO user (username, salted_password, email) VALUES (?, ?, ?)", (username, pwd_salted_hash, email))
        connection.commit()
        return c.lastrowid
    except Exception as e:
        #current_app.logger.error(f"Failed to insert the row (username {username}, pwd_salted_hash {pwd_salted_hash}, email {email}) into `user` table: {e}")
        print(f"Failed to insert the row (username {username}, salted_password {pwd_salted_hash}, email {email}) into `user` table: {e}")
        return None


def get_rating(user_id, place_id):
    #TODO 6/27/21 change the exception error message
    connection = sqlite3.connect('userinfo.db')
    # create a cursor
    c = connection.cursor()
    try:
        c.execute(f"SELECT rating_score FROM rating (user_id, place_id) VALUES (?, ?)", (user_id, place_id))
        connection.commit()
        return c.fetchone()[0]
    except Exception as e:
        #current_app.logger.error(f"Failed to retrieve the row (user_id {user_id}, place_id {place_id}) from `rating` table: {e}")
        print(f"Failed to retrieve the row (user_id {user_id}, place_id {place_id}) from `rating` table: {e}")
        return None

def update_restaurant_rating(user_id, place_id, rating):
    #TODO 6/27/21 Use INSERT_OR_REPLACE statment to update restaurant rating - there must be only 1 rating per restaurant for each user
    connection = sqlite3.connect('userinfo.db')
    # create a cursor
    c = connection.cursor()
    try:
        c.execute(f"INSERT_OR_REPLACE rating (user_id, place_id, rating) VALUES (?, ?, ?)", (user_id, place_id, rating))
        connection.commit()
        return c.lastrowid
    except Exception as e:
        #current_app.logger.error(f"Failed to insert the row (username {username}, pwd_salted_hash {pwd_salted_hash}, email {email}) into `user` table: {e}")
        print(f"Failed to insert the row (user_id {user_id}, place_id {place_id}, rating {rating}) into `user` table: {e}")
        return None

def get_unliked_rest(username):
    return 1