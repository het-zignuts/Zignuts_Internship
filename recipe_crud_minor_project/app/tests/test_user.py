from jose import jwt

def test_list_users(client, get_test_tokens):
    access_token=get_test_tokens["access_token"]
    header={"Authorization": f"Bearer {access_token}"}
    response=client.get("/users", headers=header)
    assert response.status_code==403 # as only admin can access all users and admin is not created yet

def test_get_user_me(client, get_test_tokens):
    access_token=get_test_tokens["access_token"]
    header={"Authorization": f"Bearer {access_token}"}
    response=client.get("/users/me", headers=header)
    assert response.status_code==200

def test_get_user(client, get_test_tokens, test_user):
    access_token=get_test_tokens["access_token"]
    print(jwt.decode(access_token,key="", algorithms=["HS256"], options={"verify_signature": False}))
    user_id=test_user["id"]
    header={"Authorization": f"Bearer {access_token}"}
    response=client.get(f"/users/{user_id}", headers=header)
    print(response)
    assert response.status_code==200

def test_delete_user_me(client, get_test_tokens):
    access_token=get_test_tokens["access_token"]
    header={"Authorization": f"Bearer {access_token}"}
    response=client.delete("/users/me", headers=header)
    assert response.status_code==204


