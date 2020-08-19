#pylint: disable=import-outside-toplevel,invalid-name,redefined-outer-name
"""
Sample Tests
Test the Contacts API
"""

import json
from datetime import datetime
import pytest


# this fixture just uses the sample database for read-only operations
@pytest.fixture
def api_fixture(request):
    """
    API Test Fixture
        - initialize database
        - load some test data
        - get a test client
        - authenticate
    """
    import sample
    # initialize the database and load some test data
    with sample.app.app_context():
        sample.init_db()
        with open('tests/sampledata.sql', 'r') as f:
            conn = sample.db.engine.raw_connection()
            conn.executescript(f.read())
            conn.close()
    test_client = sample.app.test_client()
    data = {
        'username': 'user2',
        'password': '4567'
    }
    rv = test_client.post('/api/login', data=json.dumps(data),
                          content_type='application/json')
    assert rv.status_code == 200
    data = json.loads(rv.data.decode('utf-8'))
    return (test_client, data['access_token'])


def test_get(api_fixture):
    """Make sure a single contact can be retrieved"""
    client, access_token = api_fixture
    rv = client.get('/api/contacts/1',
                    headers={'Authorization': 'Bearer '+access_token})
    assert rv.status_code == 200
    data = json.loads(rv.data.decode('utf-8'))
    assert 'first_name' in data
    assert data['first_name'] == 'Roy'


def test_get_all(api_fixture):
    """Make sure all contacts can be retrieved"""
    client, access_token = api_fixture
    rv = client.get('/api/contacts',
                    headers={'Authorization': 'Bearer '+access_token})
    assert rv.status_code == 200
    data = json.loads(rv.data.decode('utf-8'))
    assert len(data) == 1000


def test_put(api_fixture):
    """Make sure a new contact can be created"""
    client, access_token = api_fixture
    data = {
        'first_name': 'Sally',
        'last_name': 'Sample',
        'email': 'sally@sample.com',
        'phone': '123-555-1212',
        'created': datetime.now().isoformat()
    }
    rv = client.put('/api/contacts', data=json.dumps(data),
                    content_type='application/json',
                    headers={'Authorization': 'Bearer '+access_token})
    assert rv.status_code == 200


def test_post(api_fixture):
    """Make sure an existing contact can be updated"""
    client, access_token = api_fixture
    data = {
        'last_name': 'Updated Last Name',
        'email': 'updated.email@somewhere.com'
    }
    rv = client.post('/api/contacts/10', data=json.dumps(data),
                     content_type='application/json',
                     headers={'Authorization': 'Bearer '+access_token})
    assert rv.status_code == 200
    # make sure it actually got updated
    rv = client.get('/api/contacts/10',
                    headers={'Authorization': 'Bearer '+access_token})
    assert rv.status_code == 200
    data = json.loads(rv.data.decode('utf-8'))
    assert data['last_name'] == 'Updated Last Name'
    assert data['email'] == 'updated.email@somewhere.com'


def test_delete(api_fixture):
    """Make sure a contact can be deleted"""
    client, access_token = api_fixture
    rv = client.delete('/api/contacts/100',
                       headers={'Authorization': 'Bearer '+access_token})
    assert rv.status_code == 200
    # make sure it actually got deleted
    rv = client.get('/api/contacts/100',
                    headers={'Authorization': 'Bearer '+access_token})
    assert rv.status_code == 404
