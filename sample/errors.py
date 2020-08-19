"""
JSON Error Handlers
Replace default error handlers with JSON equivalents
Add additional error handlers as needed
"""

from werkzeug.exceptions import HTTPException
from flask.json import jsonify
from . import app

def error_handler(error):
    """
    Standard Error Handler
    """
    if isinstance(error, HTTPException):
        return jsonify({
            'statusCode': error.code,
            'name': error.name,
            'description': error.description
        }), error.code

    return jsonify({
        'statusCode': 500,
        'name': 'Internal Server Error',
        'description': 'An unknown error has occurred'
    }), 500

# common errors - add others as needed
app.register_error_handler(400, error_handler)
app.register_error_handler(401, error_handler)
app.register_error_handler(403, error_handler)
app.register_error_handler(404, error_handler)
app.register_error_handler(405, error_handler)
app.register_error_handler(500, error_handler)
