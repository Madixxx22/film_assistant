from fastapi.testclient import TestClient

from app.main import app

def test_clear_history_search():
    token_data = {
        "username": "film-assistant@example.com",
        "password": "12345"
    }

    with TestClient(app) as client:
        token_response = client.post("/log-in", data=token_data)
        token = token_response.json()["access_token"]
        response = client.delete("/clear-history-search", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

    with TestClient(app) as client:
        response = client.get("/history-search", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == []

def test_delete_selected_films():
    token_data = {
        "username": "film-assistant@example.com",
        "password": "12345"
    }

    with TestClient(app) as client:
        token_response = client.post("/log-in", data=token_data)
        token = token_response.json()["access_token"]
        response = client.delete("/selected-films/delete-selected-films?id_film=1", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

    with TestClient(app) as client:
        response = client.get("/selected-films", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == []

def test_delete_user():
    token_data = {
        "username": "film-assistant@example.com",
        "password": "12345"
    }

    with TestClient(app) as client:
        token_response = client.post("/log-in", data=token_data)
        token = token_response.json()["access_token"]
        response = client.delete("/profile-user/delete-user", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

    with TestClient(app) as client:
        response = client.get("/profile-user", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"