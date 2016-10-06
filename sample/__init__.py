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
    with app.open_resource('resources/schema.sql', 'r') as f:
        conn = db.engine.raw_connection()
        conn.executescript(f.read())
        conn.close()


# register error handlers
from . import errors  # noqa: E401,402

# register CLI commands
from . import commands  # noqa: E401,402

# initialize jwt
from . import auth  # noqa: E401,402

# load & register APIs
from .api import *  # noqa: E401,402
