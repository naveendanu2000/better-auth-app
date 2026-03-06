from fastapi.testclient import TestClient
from main import app


def test_login_returns_access_token_in_cookies_for_valid_credentials():

    with TestClient(app=app) as client:
        payload = {"username": "naveendanu", "password": "12345"}

        response = client.post("/api/auth/login", json=payload)

        assert response.status_code == 200
        assert response.json()["success"] == True
        assert "access_token" in response.cookies

def test_login_returns_with_401_status_for_invalid_credentials():

    with TestClient(app=app) as client:
        payload = {"username": "naveendanu", "password": "123456"}

        response = client.post("/api/auth/login", json=payload)

        assert response.status_code == 401
        assert response.json()["success"] == False

def test_login_returns_with_400_status_for_missing_username():

    with TestClient(app=app) as client:
        payload = {"username": "", "password": "1234"}

        response = client.post("/api/auth/login", json=payload)

        assert response.status_code == 400
        assert response.json()["success"] == False

def test_login_returns_with_400_status_for_missing_password():

    with TestClient(app=app) as client:
        payload = {"username": "naveendanu", "password": ""}

        response = client.post("/api/auth/login", json=payload)

        assert response.status_code == 400
        assert response.json()["success"] == False

def test_login_returns_with_400_status_for_missing_credentials():

    with TestClient(app=app) as client:
        payload = {"username": "naveendanu", "password": ""}

        response = client.post("/api/auth/login", json=payload)

        assert response.status_code == 400
        assert response.json()["success"] == False