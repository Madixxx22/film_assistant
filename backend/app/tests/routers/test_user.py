import pytest
import asyncio
from fastapi.testclient import TestClient

from app.main import app
from app.db.crud_user import user_crud

def test_register_done():
    request_data = {
        "login": "film-assistant",
        "email": "film-assistant@example.com",
        "password": "123456789",
        "password_verification": "123456789",
    }
    with TestClient(app) as client:
        response = client.post("/register", json=request_data)
    assert response.status_code == 201
    assert response.json()["login"] == request_data["login"]
    assert response.json()["email"] == request_data["email"]
    assert response.json()["hashed_password"] is not None

def test_register_error():
    request_data = {
        "login": "film-assistant",
        "email": "film-assistant@example.com",
        "password": "123456789",
        "password_verification": "123456789",
    }
    with TestClient(app) as client:
        response = client.post("/register", json=request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Such a user already exists"


def test_login_done_with_login():
    request_data = {
        "username": "film-assistant",
        "password": "123456789"
    }
    with TestClient(app) as client:
        response = client.post("/log-in", data=request_data)
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] is not None

def test_login_done_with_email():
    request_data = {
        "username": "film-assistant@example.com",
        "password": "123456789"
    }
    with TestClient(app) as client:
        response = client.post("/log-in", data=request_data)
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] is not None

def test_login_with_invalid_password():
    request_data = {
        "username": "film-assistant",
        "password": "12345",
    }
    with TestClient(app) as client:
        response = client.post("/log-in", data=request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"


def test_profile_user_update():
    token_data = {
        "username": "film-assistant@example.com",
        "password": "123456789"
    }
    with TestClient(app) as client:
        token_response = client.post("/log-in", data=token_data)
        token = token_response.json()["access_token"]
        response = client.put("/profile-user/update-profile-user?last_name=film&first_name=assistant", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_profile_user():
    token_data = {
        "username": "film-assistant@example.com",
        "password": "123456789"
    }
    with TestClient(app) as client:
        token_response = client.post("/log-in", data=token_data)
        token = token_response.json()["access_token"]
        response = client.get("/profile-user", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "film-assistant@example.com"
    assert response.json()["login"] == "film-assistant"
    assert response.json()["last_name"] == "film"
    assert response.json()["first_name"] == "assistant"
    assert response.json()["registered"] is not None

def test_recover_password_with_email():
    email = "film-assistant@example.com"
    request_data = {
        "password": "string",
        "password_verification": "string"
    }
    with TestClient(app) as client:
        response = client.post(f"/recover-password/{email}", json=request_data)
    assert response.status_code == 200

    request_data_email = {
        "username": "film-assistant@example.com",
        "password": "string"
    }
    with TestClient(app) as client:
        response = client.post("/log-in", data=request_data_email)
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] is not None

def test_recover_password_with_login():
    login = "film-assistant"
    request_data = {
        "password": "12345",
        "password_verification": "12345"
    }
    with TestClient(app) as client:
        response = client.post(f"/recover-password/{login}", json=request_data)
    assert response.status_code == 200

    request_data_login = {
        "username": "film-assistant",
        "password": "12345"
    }
    with TestClient(app) as client:
        response = client.post("/log-in", data=request_data_login)
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] is not None
