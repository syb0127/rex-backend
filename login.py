# check if username, password are in database
import dbquery
import rediscache 
import uuid
import hashlib
import os

ENVVAR_PWD_SALT = "PWD_SALT"

def salt_and_hash(pwd):
    m = hashlib.sha1()
    pwd_salt = os.environ[ENVVAR_PWD_SALT]
    m.update(pwd + pwd_salt)
    return m.hexdigest()

def create_user(username, password, email):
    """checks if the constraint already exists and creates user only when possible
        TODO: 6/25/21 float up the error message for different cases: username already exists, email already exists, or db fails
        """
    username_already_exists = dbquery.is_username_duplicate(username)
    if username_already_exists is None or username_already_exists:
        return None
    email_already_exists = dbquery.is_email_duplicate(email)
    if email_already_exists is None or email_already_exists:
        return None
    pwd = salt_and_hash(password)
    user_id = dbquery.insert_new_user(username, pwd, email)
    return user_id

def generate_session_token():
    session_token = str(uuid.uuid4())
    return session_token

def get_session_token(username, password):
    user_id = dbquery.get_user_id(username, salt_and_hash(password))
    if user_id == -1:
        return None
    session_token = rediscache.get_session_token(user_id)
    if session_token is None:
        session_token = generate_session_token()
        rediscache.set_session_token(user_id, session_token)
        return session_token
    return 
