import hashlib
#import UserInfo from './userinfo'

def get_user_id(username, pwd_salted_hash):
    if username == "apple":
        if pwd_salted_hash == "abcde":
            return 32337
        else:
            return -1
    else:
        return -1

shared_private_key = "ABCDEF"

def create_signature(data):
    return hashlib.sha1(repr(data) + "," + shared_private_key).hexdigest()

def verify_signature(data, signature):
    return signature == create_signature(data)

def add_user(username, pwd_salted_hash):


    username_hash = hashlib.sha256() + username
    pwd_salted_hash_con = hashlib.sha256() + pwd_salted_hash
    return
