# pylint: disable=import-outside-toplevel,invalid-name,redefined-outer-name
"""
Test Authentication Functions
"""

import json
import pytest


@pytest.fixture
def client():
    """Get a test client"""
    import sample

    # initialize the database
    app = sample.create_app()
    with app.app_context():
        sample.db.init_db()
    return app.test_client()


def test_login(client):
    """Make sure the login API authenticates user correctly"""
    data = {"username": "user1", "password": "1234"}
    rv = client.post(
        "/api/login", data=json.dumps(data), content_type="application/json"
    )
    assert rv.status_code == 200
    data = json.loads(rv.data.decode("utf-8"))
    assert "access_token" in data


def test_bad_login(client):
    """Make sure invalid credentials fail"""
    data = {"username": "user2", "password": "xyz"}
    rv = client.post(
        "/api/login", data=json.dumps(data), content_type="application/json"
    )
    assert rv.status_code == 403


def test_invalid_login(client):
    """Also make sure invalid payload is rejected"""
    data = {"username": "user2"}
    rv = client.post(
        "/api/login", data=json.dumps(data), content_type="application/json"
    )
    assert rv.status_code == 400


def test_access_granted(client):
    """Make sure we can access protected resources with a valid token"""
    data = {"username": "user2", "password": "4567"}
    rv = client.post(
        "/api/login", data=json.dumps(data), content_type="application/json"
    )
    assert rv.status_code == 200
    data = json.loads(rv.data.decode("utf-8"))
    access_token = data["access_token"]
    assert "access_token" in data
    rv = client.get("/api/auth", headers={"Authorization": "Bearer " + access_token})
    assert rv.status_code == 200
    data = json.loads(rv.data.decode("utf-8"))
    assert data["current_identity"] == "user2"


def test_access_denied_no_token(client):
    """Make sure access is denied to a protected resource without token"""
    rv = client.get("/api/auth")
    assert rv.status_code == 401


def test_access_denied_invalid_token(client):
    # pylint: disable=C0301
    """Make sure access is denied with an invalid token"""
    rv = client.get(
        "/api/auth",
        headers={
            "Authorization": "Bearer eyK0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTc4NTQ4OTQsIm5iZiI6MTU5Nzg1NDg5NCwianRpIjoiZmI4NjZlZDAtMjg0Zi00YzAzLWI3MzktMTQzNjdkMjFlZjIzIiwiZXhwIjoxNTk3ODU1Nzk0LCJpZGVudGl0eSI6InVzZXIyIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.a9FRgAtcehRAiG_b4zQK54t96VbKfx8O_sjCf5wz4o0"
        },
    )
    assert rv.status_code in [401, 422]
