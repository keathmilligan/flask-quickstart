"""
Authenticaton Functions
TODO: replace with a real authentication backend
"""

from flask_jwt import JWT
from werkzeug.security import safe_str_cmp
from . import app


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', '1234'),
    User(2, 'user2', '4567'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    """
    Authenticate a username/password - this sample routine simply checks
    the username/password against a hard-coded table, a real-world
    implementation would authenticate users against a database or external
    service.
    """
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'),
                             password.encode('utf-8')):
        return user


def identity(payload):
    """
    Get user by ID
    """
    user_id = payload['identity']
    return userid_table.get(user_id, None)


jwt = JWT(app, authenticate, identity)
