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
            salted_password VARCHAR(30),
            email VARCHAR(50) NOT NULL UNIQUE
        )""")

    connection.commit()
    connection.close()

#주어진 디비를 읽고 쓰는 역할을 함

def get_user_id(username, pwd_salted_hash):
    if username == "apple":
        if pwd_salted_hash == "abcde":
            return 32337
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
        return c.fetchone() > 0
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
        return c.fetchone() > 0
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

def get_unliked_rest(username):
    return 1