import pytest
from app import schemas
from jose import jwt
from app.config import settings  # Import settings from your app configuration


def test_root_route(client):
    res = client.get("/")
    assert res.status_code == 200


# testing login functionality


def test_user_login(client, create_user_test):
    res = client.post(
        "/login", data={"username": create_user_test["email"],
                        "password": create_user_test["password"]})
    login_data = schemas.Token(**res.json())
    payload = jwt.decode(login_data.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    assert payload.get("user_id") == create_user_test["user_id"]
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail5@gmail.com', 'password1243', 403),
    ('joeyk@gmail.com', 'wrongpassword', 403),
    ('nonexistent@gmail.com', 'wrongpassword', 403),
    (None, 'password1243', 403),
    ('joeyk@gmail.com', None, 403)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code


# testing posts methods
