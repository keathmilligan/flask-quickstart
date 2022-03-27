"""
Authenticaton Functions
TODO: replace with a real authentication backend
"""

from datetime import datetime, timedelta, timezone
from functools import wraps


from flask import (
    Blueprint,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
)
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    set_access_cookies,
    verify_jwt_in_request,
    jwt_required,
    unset_jwt_cookies,
)
from werkzeug.security import safe_str_cmp


blueprint = Blueprint("auth", __name__)


# pylint: disable=too-few-public-methods
class User:
    """Example user object"""

    def __init__(self, user_id, username, password):
        self.id = user_id  # pylint: disable=invalid-name
        self.username = username
        self.password = password

    def __str__(self):
        return f"User(id={self.id})"


users = [
    User(1, "user1", "1234"),
    User(2, "user2", "4567"),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def init_jwt(app):
    """
    Initialize JWT Manager
    """
    JWTManager(app)


def authenticate(username, password):
    """
    Authenticate a username/password - this sample routine simply checks
    the username/password against a hard-coded table, a real-world
    implementation would authenticate users against a database or external
    service.
    """
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode("utf-8"), password.encode("utf-8")):
        return create_access_token(identity=user.username)
    return None


def get_user():
    """
    Get user from identity
    """
    try:
        verify_jwt_in_request(optional=True)
        return username_table.get(get_jwt_identity(), None)
    except:  # pylint: disable=bare-except
        return None


def refresh_auth():
    """
    Create a new token from current identity
    """
    identity = get_jwt_identity()
    # TODO: confirm account is still valid/active otherwise raise an exception
    return create_access_token(identity=identity)


@blueprint.before_app_request
def get_current_user():
    """
    Load current user if someone is logged in
    """
    g.user = get_user()


@blueprint.after_app_request
def refresh_expiring_jwts(response):
    """
    Automatically refresh JWTs in cookies
    """
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


def auth_required():
    """
    Custom auth required decorator for page views
    Redirects to login page if JWT is not present or invalid
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                return fn(*args, **kwargs)
            except:  # pylint: disable=bare-except
                return redirect(url_for('index'))
        return decorator
    return wrapper


@blueprint.route("/login", methods=["GET", "POST"])
def login_page():
    """
    Login page
    """
    if request.method == "GET":
        return render_template("auth/login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        access_token = authenticate(username, password)
        if access_token is not None:
            response = redirect(url_for("index"))
            set_access_cookies(response, access_token)
            flash("Logged in")
            return response
        else:
            flash("Invalid username/password")
            return render_template("auth/login.html")


@blueprint.route("/logout", methods=["GET", "POST"])
@auth_required()
def logout_page():
    """
    Logout page
    """
    if request.method == "GET":
        return render_template("auth/logout.html")
    else:
        response = redirect(url_for("index"))
        flash("Logged out")
        unset_jwt_cookies(response)
        return response


# API-Oriented Views
# Delete these if you don't need to provide RESTful APIs

@blueprint.route("/api/login", methods=["POST"])
def login():
    """
    Login API
    """
    data = request.get_json()
    if "username" in data and "password" in data:
        username = data["username"]
        password = data["password"]
        access_token = authenticate(username, password)
        if access_token is not None:
            refresh_token = create_refresh_token(username)
            return jsonify({"access_token": access_token, "refresh_token": refresh_token})
        else:
            abort(403)
    else:
        abort(400)


@blueprint.route("/api/auth", methods=["GET"])
@jwt_required()
def auth_check():
    """Test function to verify authentication status"""
    user = get_user()
    return jsonify({"current_identity": user.username})


@blueprint.route("/api/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    return jsonify({"access_token": refresh_auth()})
