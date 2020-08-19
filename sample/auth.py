"""
Authenticaton Functions
TODO: replace with a real authentication backend
"""

from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from werkzeug.security import safe_str_cmp
from . import app


class User:
    """Example user object"""
    def __init__(self, user_id, username, password):
        self.id = user_id  # pylint: disable=invalid-name
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
        return create_access_token(identity=user.username)
    return None


def get_user():
    """
    Get user from identity
    """
    return username_table.get(get_jwt_identity(), None)


jwt = JWTManager(app)
