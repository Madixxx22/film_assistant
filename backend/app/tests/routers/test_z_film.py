from fastapi.testclient import TestClient

from app.main import app


def test_add_film_selected():
    token_data = {
        "username": "film-assistant@example.com",
        "password": "12345"
    }

    request_data =   {
        "name_film": "Kingsman: The Secret Service",
        "genres": [
            "Action",
            "Adventure",
            "Comedy"
        ],
        "rating": 7.7,
        "img_link": "https://imdb-api.com/images/original/MV5BYTM3ZTllNzItNTNmOS00NzJiLTg1MWMtMjMxNDc0NmJhODU5XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_Ratio0.6837_AL_.jpg"
  }
    with TestClient(app) as client:
        token_response = client.post("/log-in", data=token_data)
        token = token_response.json()["access_token"]
        response = client.post("/add-film-selected", headers={"Authorization": f"Bearer {token}"}, json=request_data)

    assert response.status_code == 201

def test_film_search():
    token_data = {
        "username": "film-assistant@example.com",
        "password": "12345"
    }

    request_data =   {
        "name_film": "Kingsman",
        "genres": [
            "Action",
            "Comedy"
        ],
        "rating_start": 7,
        "rating_end": 8.0
  }
    with TestClient(app) as client:
        token_response = client.post("/log-in", data=token_data)
        token = token_response.json()["access_token"]
        response = client.post("/film-search", headers={"Authorization": f"Bearer {token}"}, json=request_data)

    assert response.status_code == 200
    assert response.json()[0]["name_film"] == "Kingsman: The Secret Service"
    assert response.json()[0]["genres"] == ["Action", "Adventure", "Comedy"]
    assert response.json()[0]["rating"] == 7.7
    assert response.json()[0]["img_link"] == "https://imdb-api.com/images/original/MV5BYTM3ZTllNzItNTNmOS00NzJiLTg1MWMtMjMxNDc0NmJhODU5XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_Ratio0.6837_AL_.jpg"

def test_history_search():
    token_data = {
        "username": "film-assistant@example.com",
        "password": "12345"
    }

    with TestClient(app) as client:
        token_response = client.post("/log-in", data=token_data)
        token = token_response.json()["access_token"]
        response = client.get("/history-search", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()[0]["name_film"] == "Kingsman"
    assert response.json()[0]["genres"] == ["Action", "Comedy"]
    assert response.json()[0]["rating_start"] == 7.0
    assert response.json()[0]["rating_end"] == 8.0

def test_history_search_film():
    token_data = {
        "username": "film-assistant@example.com",
        "password": "12345"
    }

    with TestClient(app) as client:
        token_response = client.post("/log-in", data=token_data)
        token = token_response.json()["access_token"]
        response = client.get("/history-search/film-history-by-search?id_search=1", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()[0]["name_film"] == "Kingsman: The Secret Service"
    assert response.json()[0]["genres"] == ["Action", "Adventure", "Comedy"]
    assert response.json()[0]["rating"] == 7.7
    assert response.json()[0]["img_link"] == "https://imdb-api.com/images/original/MV5BYTM3ZTllNzItNTNmOS00NzJiLTg1MWMtMjMxNDc0NmJhODU5XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_Ratio0.6837_AL_.jpg"

def test_selected_films():
    token_data = {
        "username": "film-assistant@example.com",
        "password": "12345"
    }

    with TestClient(app) as client:
        token_response = client.post("/log-in", data=token_data)
        token = token_response.json()["access_token"]
        response = client.get("/selected-films", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()[0]["name_film"] == "Kingsman: The Secret Service"
    assert response.json()[0]["genres"] == ["Action", "Adventure", "Comedy"]
    assert response.json()[0]["rating"] == 7.7
    assert response.json()[0]["img_link"] == "https://imdb-api.com/images/original/MV5BYTM3ZTllNzItNTNmOS00NzJiLTg1MWMtMjMxNDc0NmJhODU5XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_Ratio0.6837_AL_.jpg"

def test_recommendations():
    token_data = {
        "username": "film-assistant@example.com",
        "password": "12345"
    }

    with TestClient(app) as client:
        token_response = client.post("/log-in", data=token_data)
        token = token_response.json()["access_token"]
        response = client.get("/recommendations", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()[0]["name_film"] is not None
    assert response.json()[0]["genres"] is not None
    assert response.json()[0]["rating"] is not None
    assert response.json()[0]["img_link"] is not None
