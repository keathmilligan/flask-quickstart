# pylint: disable=C0413
"""
Flask Quick-Start Template
Application bootstrap
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_json('../config.json')
db = SQLAlchemy(app)
ma = Marshmallow(app)


def init_db():
    """Initialize the database"""
    with app.open_resource('resources/schema.sql', 'r') as schema:
        conn = db.engine.raw_connection()
        conn.executescript(schema.read())
        conn.close()


# register error handlers
from . import errors

# register CLI commands
from . import commands

# initialize jwt
from . import auth

# load & register APIs
from .api import *
