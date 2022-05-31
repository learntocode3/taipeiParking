from functools import wraps
from flask import Flask, make_response, request
import sys
sys.path.append('./')
from settings import MIDDLEWARE_USERNAME, MIDDLEWARE_PASSWORD



def middleware(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):

        auth = request.authorization

        if auth and auth.username == MIDDLEWARE_USERNAME and auth.password == MIDDLEWARE_PASSWORD:
            return func(*args, **kwargs)

        return make_response('Authorization failed', 401, {'WWW-Authenticate':'Basic realm="Login Required'})

    return decorated_function