import pytest
from uuid import uuid4, UUID
from jose import jwt
from app.core.config import Config

@pytest.fixture(scope="session")
def test_create_recipe(client, test_user, get_test_tokens):
    access_token = get_test_tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
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
    assert response.status_code == 201
    return response.json()

def test_get_recipe(client, get_test_tokens, test_recipe):
    access_token=get_test_tokens["access_token"]
    header={"Authorization": f"Bearer {access_token}"}
    recipe_id=test_recipe["id"]
    response=client.get(f"/recipes/{recipe_id}", headers=header)
    print(response.json())
    assert response.status_code==200

def test_list_recipes(client, get_test_tokens):
    access_token=get_test_tokens["access_token"]
    header={"Authorization": f"Bearer {access_token}"}
    response=client.get(f"/recipes/", headers=header)
    assert response.status_code==200

def test_update_recipe(client, get_test_tokens, test_recipe):
    access_token=get_test_tokens["access_token"]
    header={"Authorization": f"Bearer {access_token}"}
    recipe_id=test_recipe["id"]
    req_data={
        "title": "test_recipe2_"+str(uuid4().hex),
        "description": "It's delicioussss...",
        "ingredients": ["Love", "Life", "Lafda"],
        "instructions": "live and let live...",
        "time_taken": 223322,
        "serving": "2 lifetimes",
        "cuisine": "universal",
        "category": "snack",
        "image_url": None
    }
    response=client.put(f"/recipes/{recipe_id}", json=req_data, headers=header)
    assert response.status_code==200

def test_partial_update_recipe(client, get_test_tokens, test_recipe):
    access_token=get_test_tokens["access_token"]
    header={"Authorization": f"Bearer {access_token}"}
    recipe_id=test_recipe["id"]
    req_data={
        "cuisine": "multiversal",
        "category": "dinner"
    }
    response=client.patch(f"/recipes/{recipe_id}", json=req_data, headers=header)
    assert response.status_code==200

def test_delete_recipe(client, get_test_tokens, test_recipe):
    access_token=get_test_tokens["access_token"]
    payload = jwt.decode(access_token, key="", algorithms=[Config.ALGORITHM], options={"verify_signature": False})
    print("token user:", payload["sub"])
    print("recipe user:", test_recipe["uploaded_by"])
    header={"Authorization": f"Bearer {access_token}"}
    recipe_id=test_recipe["id"]
    response=client.delete(f"/recipes/{recipe_id}", headers=header)
    assert response.status_code==200

