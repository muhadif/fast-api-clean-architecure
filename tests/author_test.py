def test_get_author(client):
    response = client.get("/api/authors")
    assert response.status_code == 200
    assert response.json() == {'authors': [{'bio': 'hi', 'birthdate': '2024-06-20', 'id': 1, 'name': 'adif'},
                                           {'bio': 'hello', 'birthdate': '2023-06-20', 'id': 2, 'name': 'adif-2'}],
                               'page': 1, 'pageSize': 10, 'total': 2}


def test_get_author_with_name_query(client):
    response = client.get("/api/authors?name=adif")
    assert response.status_code == 200
    assert len(response.json()["authors"]) == 1
    assert response.json()["authors"][0]["name"] == "adif"


def test_get_by_id_author(client):
    response = client.get("/api/authors/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "adif"


def test_get_by_id_author_error_not_found(client):
    response = client.get("/api/authors/200")
    assert response.status_code == 404
    assert response.json()["detail"] == "Author not found"


def test_create_author(client):
    data = {
        "name": "adif new",
        "bio": "bio",
        "birthdate": "2024-06-20"
    }
    response = client.post("api/authors", json=data)
    assert response.status_code == 200
    assert response.json()["id"] is not None

def test_create_author_name_is_empty(client):
    data = {
        "bio": "bio",
        "birthdate": "2024-06-20"
    }
    response = client.post("api/authors", json=data)
    assert response.status_code == 422

def test_create_author_wrong_dateformat(client):
    data = {
        "bio": "bio",
        "birthdate": "2024-06---20"
    }
    response = client.post("api/authors", json=data)
    assert response.status_code == 422

def test_update_author(client):
    data = {
      "id": 1,
      "name": "adif aja",
      "bio": "new bio",
      "birthdate": "2021-06-20T12:00:00"
    }
    response = client.put("api/authors/1", json=data)
    assert response.status_code == 200
    assert response.json() == {'bio': 'new bio', 'birthdate': '2021-06-20T12:00:00', 'id': 1, 'name': 'adif aja'}

def test_delete_author(client):
    response = client.delete("api/authors/3")
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}