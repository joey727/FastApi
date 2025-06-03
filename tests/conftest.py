"""set fixtures here for pytest"""

from fastapi.testclient import TestClient
import pytest
from app.database import Base, get_db
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.oauth2 import create_access_token
from app import models


# test database for testing routes
DATABASE_URL = (
    f"postgresql://{settings.database_username}:"
    f"{settings.database_password}@{settings.database_hostname}:"
    f"{settings.database_port}/{settings.database_name}_test"
)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


# testing creating user route
@pytest.fixture
def create_user_test2(client):
    data = {"email": "anna33@gmail.com", "password": "password1243"}
    res = client.post(
        "/create", json=data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = data["password"]
    return new_user


@pytest.fixture
def create_user_test(client):
    data = {"email": "joeyk@gmail.com", "password": "password1243"}
    res = client.post(
        "/create", json=data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = data["password"]
    return new_user


@pytest.fixture
def token(create_user_test):
    # return create_access_token()
    return create_access_token({"user_id": create_user_test['user_id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(create_user_test, session, create_user_test2):
    data = [
        {
            "title": "something something",
            "content": "anything here",
            "owner_id": create_user_test['user_id']
        },
        {
            "title": "summertime",
            "content": "it's always fun and games",
            "owner_id": create_user_test['user_id']
        },
        {
            "title": "making wealth",
            "content": "gotta lock in",
            "owner_id": create_user_test2["user_id"]
        }
    ]

    posts = [models.Post(**post) for post in data]
    session.add_all(posts)
    session.commit()
    return session.query(models.Post).all()
