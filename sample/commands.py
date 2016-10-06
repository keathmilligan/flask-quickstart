"""
Sample App Commands
Add extra "flask" commands here (db initialization, maintenance, etc.)
"""

from . import app, init_db

@app.cli.command('initdb')
def initdb_command():
    """Initialize the database schema"""
    init_db()
    print('Database initialized')
