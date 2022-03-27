"""
Serve app with waitress
"""

from waitress import serve
from . import create_app


if __name__ == "__main__":
    print('Serving app with waitress')
    app = create_app()
    serve(app)
