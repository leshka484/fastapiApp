import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.database import Base
from app.main import app, get_db

load_dotenv()

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_crud_user():
    # post
    response = client.post(
        "/users/",
        json={"name": "user", "email": "user@example.com", "password": "string"},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "user"
    assert data["email"] == "user@example.com"
    assert "id" in data
    user_id = data["id"]

    # get
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "user"
    assert data["email"] == "user@example.com"
    assert data["id"] == user_id

    # put
    response = client.put(
        f"/users/{user_id}",
        json={"name": "user2", "email": "user2@example.com", "password": "string2"},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "user2"
    assert data["email"] == "user2@example.com"

    # delete
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == {"message": "user user2 was deleted"}
