

def get_user_id(username, pwd_salted_hash):
    if username == "apple":
        if pwd_salted_hash == "abcde":
            return 32337
        else:
            return -1
    else:
        return -1
