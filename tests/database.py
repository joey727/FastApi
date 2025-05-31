# from fastapi.testclient import TestClient
# import pytest
# from app.database import Base, get_db
# from app.main import app
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.config import settings

# # test database for testing routes
# DATABASE_URL = (
#     f"postgresql://{settings.database_username}:"
#     f"{settings.database_password}@{settings.database_hostname}:"
#     f"{settings.database_port}/{settings.database_name}_test"
# )

# # Create the SQLAlchemy engine
# engine = create_engine(DATABASE_URL)

# # Create a configured "Session" class
# TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @pytest.fixture()
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @pytest.fixture()
# def client(session):
#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close()

#     app.dependency_overrides[get_db] = override_get_db

#     yield TestClient(app)
