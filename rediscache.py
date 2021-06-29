import redis
import os

ENVVAR_REDIS_HOST = "REDIS_HOST"
r = redis.Redis(host=os.environ[ENVVAR_REDIS_HOST], port=6379, db=0)

def get_session_token(user_id):
    """receives user_id and checks if it exists in cache
        if it exists, return the associated session token
        else return None
    """
    token = r.get(user_id)
    return token

def set_session_token(user_id, session_token):
    return r.set(session_token, user_id, ex=600) 

def get_user_id_by_session_token(session_token):
    user_id = r.get(session_token)
    return user_id