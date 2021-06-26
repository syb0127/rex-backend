import dbquery

def validate_signup(username, password, email):
    if username and password:
        return True, []
    elif not username:
        return False, ["Username is empty."]
    else:
        return False, ["Password is empty."]

def validate_login(username, password):
    if username and password:
        return True, []
    elif not username:
        return False, ["Username is empty."]
    else:
        return False, ["Password is empty."]
