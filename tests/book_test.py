def test_get_book(client):
    response = client.get("/api/books")
    assert response.status_code == 200
    assert len(response.json()["books"]) == response.json()["total"]


def test_get_book_with_author_query(client):
    response = client.get("/api/books?author_id=1")
    assert response.status_code == 200
    assert len(response.json()["books"]) == 1
    assert response.json()["books"][0]["title"] == "Journal"


def test_get_by_id_book(client):
    response = client.get("/api/books/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Diary"


def test_get_by_id_book_not_found(client):
    response = client.get("/api/books/200")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_create_books(client):
    data = {
        "title": "adif book 1",
        "description": "dasdssdaddas",
        "author_id": 1,
        "publish_date": "2024-06-20T12:00:00"
    }
    response = client.post("/api/books", json=data)
    assert response.status_code == 200
    assert response.json()["id"] is not None
    assert response.json()["title"] == data["title"]


def test_create_books_validation_error(client):
    data = {
        "description": "dasdssdaddas",
        "author_id": 1,
        "publish_date": "2024-06-20T12:00:00"
    }
    response = client.post("/api/books", json=data)
    assert response.status_code == 422


def test_update_books(client):
    data = {
        "id": 1,
        "title": "Dairy already updated",
        "description": "updated now",
        "author_id": 2,
        "publish_date": "2012-06-20T12:00:00"
    }
    response = client.put("/api/books/1", json=data)
    assert response.status_code == 200
    assert response.json()["id"] == data["id"]
    assert response.json()["title"] == data["title"]


def test_delete_books(client):
    response = client.delete("/api/books/3")
    assert response.status_code == 200
