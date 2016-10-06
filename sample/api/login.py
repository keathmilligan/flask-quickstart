"""
Login/Logout APIs
"""

from flask import request, jsonify, abort
from flask_jwt import jwt_required, current_identity
from .. import app
from ..auth import jwt


@app.route('/api/login', methods=['POST'])
def login():
    """
    Authenticate user and return token
    """
    data = request.get_json()
    if 'username' in data and 'password' in data:
        username = data['username']
        password = data['password']
        identity = jwt.authentication_callback(username, password)
        if identity:
            access_token = jwt.jwt_encode_callback(identity)
            return jsonify({'access_token': access_token.decode('utf-8')})
        else:
            abort(403)
    else:
        abort(400)


@app.route('/api/auth', methods=['GET'])
@jwt_required()
def authcheck():
    """Test function to verify authentication status"""
    return jsonify({'current_identity': current_identity.username})
