import pytest

# def test_create_book(client, get_test_tokens, test_user):
#     access_token=get_test_tokens["access_token"]
#     header={"Authorization": f"Bearer {access_token}"}
#     req_data={
#         "title": "test_book1",
#         "author": "tester1",
#         "isbn": "1234567",
#         "publication_year": 2025,
#         "owner_id": str(test_user["id"])
#         }
#     response=client.post("/books/", json=req_data, headers=header)
#     assert response.status_code==200

@pytest.fixture(scope="session")
def test_create_book(client, test_user, get_test_tokens):
    access_token = get_test_tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    book_req_data = {
        "title": "test_book",
        "author": "tester",
        "isbn": "123test",
        "publication_year": 2025,
    }

    response = client.post("/books/", json=book_req_data, headers=headers)
    assert response.status_code == 201
    return response.json()

def test_get_book(client, get_test_tokens, test_book):
    access_token=get_test_tokens["access_token"]
    header={"Authorization": f"Bearer {access_token}"}
    book_id=test_book["id"]
    response=client.get(f"/books/{book_id}", headers=header)
    print(response.json())
    assert response.status_code==200

def test_list_books(client, get_test_tokens):
    access_token=get_test_tokens["access_token"]
    header={"Authorization": f"Bearer {access_token}"}
    response=client.get(f"/books/", headers=header)
    assert response.status_code==200

def test_update_book(client, get_test_tokens, test_book):
    access_token=get_test_tokens["access_token"]
    header={"Authorization": f"Bearer {access_token}"}
    book_id=test_book["id"]
    req_data={
        "title": "new_title",
        "author": "new_author",
        "isbn": "string1",
        "publication_year": 2002
    }
    response=client.put(f"/books/{book_id}", json=req_data, headers=header)
    assert response.status_code==200

def test_partial_update_book(client, get_test_tokens, test_book):
    access_token=get_test_tokens["access_token"]
    header={"Authorization": f"Bearer {access_token}"}
    book_id=test_book["id"]
    req_data={
        "author": "the_author",
        "publication_year": 2004
    }
    response=client.patch(f"/books/{book_id}", json=req_data, headers=header)
    assert response.status_code==200

def test_delete_book(client, get_test_tokens, test_book):
    access_token=get_test_tokens["access_token"]
    header={"Authorization": f"Bearer {access_token}"}
    book_id=test_book["id"]
    response=client.delete(f"/books/{book_id}", headers=header)
    assert response.status_code==200

