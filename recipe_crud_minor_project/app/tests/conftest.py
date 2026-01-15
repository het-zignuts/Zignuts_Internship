import pytest
from sqlmodel import Session, create_engine, SQLModel
from app.db.session import DatabaseSession
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.core.security import Security
from uuid import uuid4 
from app.core.config import Config
from jose import jwt
from app.db.session import db_session_manager

engine=db_session_manager.engine
print("TEST DB INSTANCE ID:", id(db_session_manager))

@pytest.fixture(scope="session", autouse=True)
def db_engine():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="session")
def db_session(db_engine):
    with Session(db_engine) as session:
        yield session       

def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[db_session_manager.get_session] = override_get_session

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(scope="function")
def test_user(db_session):
    user=User(
        email= f"test_{uuid4().hex}@pytest.com",
        user_name=f"user_{uuid4().hex}",
        password= Security.hash_password("password@testuser"),
        role="user"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "user_name": user.user_name,
        "password": "password@testuser"
    }

@pytest.fixture(scope="function")
def get_test_tokens(client, test_user):
    req_data={
        "email": test_user["email"],
        "user_name": test_user["user_name"],
        "password": test_user["password"]
    }
    response=client.post("/auth/login", json=req_data)
    response_tkns=response.json()
    payload = jwt.decode(response_tkns["access_token"], key="", algorithms=[Config.ALGORITHM], options={"verify_signature": False})

    assert payload["sub"] == str(test_user["id"])
    return response.json()

@pytest.fixture(scope="function")
def test_recipe(client, test_user, get_test_tokens):
    access_token = get_test_tokens["access_token"]
    header = {"Authorization": f"Bearer {access_token}"}
    recipe_req_data={
        "title": "test_recipe_"+str(uuid4().hex),
        "description": "It's delicious...",
        "ingredients": ["Love", "Life", "Lafda"],
        "instructions": "live and let live...",
        "time_taken": 22332,
        "serving": "1 lifetime",
        "cuisine": "universal",
        "category": "snack",
        "image_url": None
    }
    response=client.post("/recipes/", json=recipe_req_data, headers=header)
    assert response.status_code == 200
    response_data=response.json()
    return response.json()



