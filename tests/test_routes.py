import pytest
from app import models, schemas
from jose import jwt
from app.config import settings
from app.routers import auth
from tests.conftest import session  # Import settings from your app configuration


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
def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts")
    assert res.status_code == 200
    posts = res.json()
    assert len(posts) == len(test_posts)
    for post in posts:
        assert isinstance(post, dict)
        assert "Post" in post
        assert "Votes" in post
        assert "id" in post["Post"]
        assert "title" in post["Post"]
        assert "content" in post["Post"]
        assert "owner" in post["Post"]


def test_unauthorized_user_get_posts(client, test_posts):
    res = client.get("/posts")
    assert res.status_code == 401


def test_unauthorized_get_post_by_id(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_post_by_validID(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    post = res.json()
    assert post["Post"]["id"] == test_posts[0].id
    assert post["Post"]["title"] == test_posts[0].title
    assert post['Post']['content'] == test_posts[0].content
    assert post['Post']['owner']['user_id'] == test_posts[0].owner.user_id


def test_get_posts_by_unexistentID(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/800000")
    assert res.status_code == 404


@pytest.mark.parametrize("title, content, published", [
    ("awesome", "somthing nice", False),
    ("Accra life", "nightlife and restaurants", True),
    ("supacars", "porsche is the best", True)
])
def test_create_post(authorized_client, title, content, published, create_user_test):
    res = authorized_client.post(
        "/posts", json={"title": title, "content": content, "published": published})
    data = res.json()
    assert res.status_code == 201
    assert data["title"] == title
    assert data["content"] == content
    assert data["published"] == published
    assert data['owner']['user_id'] == create_user_test['user_id']


def test_unauthorized_user_create_post(client):
    res = client.post(
        "/posts/", json={"title": "some title", "content": "some content"})

    assert res.status_code == 401


def test_unathorized_user_post_delete(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_post_delete_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_unexitent_post(authorized_client):
    res = authorized_client.delete("/posts/8399995")
    assert res.status_code == 404


def test_delete_post_other_owner(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[2].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts):
    data = {
        "title": "new title",
        "content": "new content"
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_post_other_user(authorized_client, test_posts):
    data = {
        "title": "new title",
        "content": "new content"
    }
    res = authorized_client.put(f"/posts/{test_posts[2].id}", json=data)
    assert res.status_code == 403


# testing voting routes


def test_vote(authorized_client, test_posts, session):
    # Cast a vote for the post
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[1].id, "dir": 1})
    assert res.status_code == 201
