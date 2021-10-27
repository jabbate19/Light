from functools import wraps
from flask import session


def csh_user_auth(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        uid = str(session["userinfo"].get("preferred_username", ""))
        last = str(session["userinfo"].get("family_name", ""))
        first = str(session["userinfo"].get("given_name", ""))
        picture = "https://profiles.csh.rit.edu/image/" + uid
        auth_dict = {
            "uid": uid,
            "first": first,
            "last": last,
            "picture": picture
        }
        kwargs["auth_dict"] = auth_dict
        return func(*args, **kwargs)
    print("a")
    return wrapped_function

def latin_to_utf8(string):
    return str(bytes(string, encoding='latin1'), encoding='utf8')
