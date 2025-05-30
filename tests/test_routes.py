from tests.database import client, session

# testing root route


def test_root_route(client):
    res = client.get("/")
    assert res.status_code == 200


# testing creating user route


def test_create_user(client):
    res = client.post(
        "/create", json={"email": "joeyk@gmail.com", "password": "password1243"})
    assert res.status_code == 201


# testing login functionality


def test_user_login(client):
    res = client.post(
        "/login", data={"username": "joeyk@gmail.com", "password": "password1243"})

    assert res.status_code == 200
