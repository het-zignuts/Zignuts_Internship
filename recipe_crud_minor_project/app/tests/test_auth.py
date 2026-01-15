from uuid import uuid4

def test_register_user(client):
    req_data={
        "email": f"user{uuid4().hex}@registration.com",
        "user_name": f"user_{uuid4().hex}",
        "password":"password@user121"
    }
    response=client.post("/auth/register", json=req_data)
    assert response.status_code==200
    response_data=response.json()
    assert response_data["email"]==req_data["email"]
    assert "id" in response_data
    assert "role" in response_data

def test_invalid_registration(client, test_user):
    req_data = {
        "email": test_user["email"],
        "user_name": test_user["user_name"],
        "password": test_user["password"]
    }
    resp = client.post("/auth/register", json=req_data)
    assert resp.status_code == 400

def test_login_user(client, test_user):
    req_data={
        "email": test_user["email"],
        "user_name": test_user["user_name"],
        "password": test_user["password"]
    }
    response=client.post("/auth/login", json=req_data)
    assert response.status_code==200
    response_data=response.json()
    assert "access_token" in response_data
    assert "refresh_token" in response_data
    assert response_data["token_type"]=="bearer"

def test_invalid_user(client):
    req_data={
        "email": "user2@invalidmail.com",
        "user_name": "user2@invalid",
        "password": "pwdvalid@password"
    }
    response=client.post("/auth/login", json=req_data)
    assert response.status_code==400
    req2_data={
        "email": "testuser@pytest.com",
        "user_name": "testInvaliduser",
        "password": "invalid@password"
    }
    response2=client.post("/auth/login", json=req2_data)
    assert 400==response2.status_code

def test_refresh_token(client, get_test_tokens):
    req_data={
        "refresh_token": get_test_tokens["refresh_token"]
    }
    response=client.post("/auth/refresh", json=req_data)
    assert response.status_code==200
    response_data=response.json()
    assert "access_token" in response_data
    assert "refresh_token" in response_data
    assert response_data["token_type"]=="bearer"
