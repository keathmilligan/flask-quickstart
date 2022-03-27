"""
Flask Quick-Start Template
Application bootstrap
"""

import json
import os.path
from flask import Flask, render_template


def create_app():
    """
    Create application
    """
    app = Flask(__name__)
    app.config.from_file(os.path.join(app.root_path, "..", "config.json"), json.load)

    # pylint: disable=import-outside-toplevel,wrong-import-position,unused-import

    # setup database
    from . import db

    db.init_app(app)

    # setup authentication
    from . import auth

    auth.init_jwt(app)

    # register blueprints
    app.register_blueprint(auth.blueprint)
    from . import contacts

    app.register_blueprint(contacts.blueprint)

    # register index route
    @app.route("/")
    def index():
        """Sample app index"""
        return render_template("index.html")

    return app
