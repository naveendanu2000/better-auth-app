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
        payload = {}

        response = client.post("/api/auth/login", json=payload)

        assert response.status_code == 400
        assert response.json()["success"] == False


def test_signup_returns_with_400_status_for_missing_signup_details():

    with TestClient(app=app) as client:
        payload = {}

        response = client.post("/api/auth/signup", json=payload)

        assert response.status_code == 400
        assert response.json()["success"] == False


def test_signup_returns_with_400_status_for_missing_username():

    with TestClient(app=app) as client:
        payload = {"password": "1234567", "email": "naveendanu2000@gmail.com"}

        response = client.post("/api/auth/signup", json=payload)

        assert response.status_code == 400
        assert response.json()["success"] == False


def test_signup_returns_with_400_status_for_missing_password():

    with TestClient(app=app) as client:
        payload = {"username": "abcde", "email": "abcde@gmail.com"}

        response = client.post("/api/auth/signup", json=payload)

        assert response.status_code == 400
        assert response.json()["success"] == False


def test_signup_returns_with_400_status_for_missing_email():

    with TestClient(app=app) as client:
        payload = {"username": "abcde", "password": "123123123"}

        response = client.post("/api/auth/signup", json=payload)

        assert response.status_code == 400
        assert response.json()["success"] == False


def test_signup_returns_with_400_status_for_invalid_email():

    with TestClient(app=app) as client:
        payload = {"username": "abcde", "email": "asdasdasd", "password": "123123123"}

        response = client.post("/api/auth/signup", json=payload)

        assert response.status_code == 400
        assert response.json()["success"] == False

def test_signup_returns_with_400_status_for_invalid_password():

    with TestClient(app=app) as client:
        payload = {"username": "abcde", "email": "asdasdasd", "password": "123123123123123123123123"}

        response = client.post("/api/auth/signup", json=payload)

        assert response.status_code == 400
        assert response.json()["success"] == False

def test_signup_returns_with_400_status_for_invalid_username():

    with TestClient(app=app) as client:
        payload = {"username": "ab", "email": "asdasdasd", "password": "123123123123123123123123"}

        response = client.post("/api/auth/signup", json=payload)

        assert response.status_code == 400
        assert response.json()["success"] == False


def test_signup_returns_with_409_status_for_existing_username_and_email():

    with TestClient(app=app) as client:
        payload = {
            "username": "naveendanu",
            "password": "1234567",
            "email": "naveendanu2000@gmail.com",
        }

        response = client.post("/api/auth/signup", json=payload)

        assert response.status_code == 409
        assert response.json()["success"] == False
