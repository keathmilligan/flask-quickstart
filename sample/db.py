"""
Flask Sample App - Database Handling
"""

import os.path
from flask import current_app
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import click


def init_db():
    """
    Create database schema if it does not already exist
    """
    with current_app.open_resource(
        os.path.join("resources", "schema.sql"), "r"
    ) as schema:
        conn = db.engine.raw_connection()
        conn.executescript(schema.read())
        conn.close()


@click.command("initdb")
@with_appcontext
def initdb_command():
    """Initialize the database schema"""
    init_db()
    print("Database initialized")


def init_app(app):
    """
    App db initialization
    """
    global db, ma  # pylint: disable=global-variable-undefined
    db = SQLAlchemy(app)
    ma = Marshmallow(app)
    app.cli.add_command(initdb_command)
