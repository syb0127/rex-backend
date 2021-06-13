# check if username, password are in database
from dbquery import get_user_id

def salt_and_hash(pwd):

    return "abcde"

def get_session_token(username, password):
    user_id = get_user_id(username, salt_and_hash(password))
    if user_id == -1:
        return None
    elif user_id : #if user_id exists in cache, return that session_uuid.
        return "QWDR"
    else:
        session_uuid = "GXCV"
        #add user_id,session_uuid pair to cache
        return session_uuid
