"""
Login/Logout APIs
"""

from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required
from .. import app
from ..auth import authenticate, get_user


@app.route('/api/login', methods=['POST'])
def login():
    """
    Authenticate user and return token
    """
    data = request.get_json()
    if 'username' in data and 'password' in data:
        username = data['username']
        password = data['password']
        access_token = authenticate(username, password)
        if access_token is not None:
            print('access token: ' + access_token)
            return jsonify({'access_token': access_token})
        else:
            abort(403)
    else:
        abort(400)


@app.route('/api/auth', methods=['GET'])
@jwt_required
def authcheck():
    """Test function to verify authentication status"""
    user = get_user()
    return jsonify({'current_identity': user.username})
