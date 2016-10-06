"""
Test Authentication Functions
"""

import pytest
import json


@pytest.fixture
def client(request):
    """Get a test client"""
    import sample
    # initialize the database
    with sample.app.app_context():
        sample.init_db()
    return sample.app.test_client()


def test_login(client):
    """Make sure the login API authenticates user correctly"""
    data = {
        'username': 'user1',
        'password': '1234'
    }
    rv = client.post('/api/login', data=json.dumps(data),
                     content_type='application/json')
    assert rv.status_code == 200
    data = json.loads(rv.data.decode('utf-8'))
    assert 'access_token' in data


def test_bad_login(client):
    """Make sure invalid credentials fail"""
    data = {
        'username': 'user2',
        'password': 'xyz'
    }
    rv = client.post('/api/login', data=json.dumps(data),
                     content_type='application/json')
    assert rv.status_code == 403


def test_invalid_login(client):
    """Also make sure invalid payload is rejected"""
    data = {
        'username': 'user2'
    }
    rv = client.post('/api/login', data=json.dumps(data),
                     content_type='application/json')
    assert rv.status_code == 400


def test_access_granted(client):
    """Make sure we can access protected resources with a valid token"""
    data = {
        'username': 'user2',
        'password': '4567'
    }
    rv = client.post('/api/login', data=json.dumps(data),
                     content_type='application/json')
    assert rv.status_code == 200
    data = json.loads(rv.data.decode('utf-8'))
    access_token = data['access_token']
    assert 'access_token' in data
    rv = client.get('/api/auth',
                    headers={'Authorization': 'JWT '+access_token})
    assert rv.status_code == 200
    data = json.loads(rv.data.decode('utf-8'))
    assert data['current_identity'] == 'user2'


def test_access_denied_no_token(client):
    """Make sure access is denied to a protected resource without token"""
    rv = client.get('/api/auth')
    assert rv.status_code == 401


def test_access_denied_invalid_token(client):
    """Make sure access is denied with an invalid token"""
    rv = client.get('/api/auth',
                    headers={'Authorization': 'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNDQ0OTE3NjQwLCJuYmYiOjE0NDQ5MTc2NDAsImV4cCI6MTQ0NDkxNzk0MH0.KPmI6WSjRjlpzecPvs3q_T3cJQvAgJvaQAPtk1abC_E'})  # noqa:E501
    assert rv.status_code == 401
