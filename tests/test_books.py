import pytest
from fastapi import status

@pytest.fixture
def test_book():
    return {
        "title": "Test Book",
        "author": "Test Author",
        "published_date": "2024-01-17",
        "summary": "Test summary",
        "genre": "Test Genre"
    }

def test_create_book(authorized_client, test_book):
    response = authorized_client.post("/api/v1/books/", json=test_book)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_book["title"]
    assert "id" in data

def test_get_book(authorized_client, test_book):
    # First create a book
    response = authorized_client.post("/api/v1/books/", json=test_book)
    created_book = response.json()
    
    # Then get it
    response = authorized_client.get(f"/api/v1/books/{created_book['id']}")
    assert response.status_code == 200
    assert response.json() == created_book

def test_get_books_pagination(authorized_client, test_book):
    # Create multiple books
    for i in range(3):
        test_book["title"] = f"Test Book {i}"
        authorized_client.post("/api/v1/books/", json=test_book)
    
    response = authorized_client.get("/api/v1/books/?page=1")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert "page" in data
    assert "pages" in data
    assert len(data["items"]) > 0

def test_update_book(authorized_client, test_book):
    # First create a book
    response = authorized_client.post("/api/v1/books/", json=test_book)
    created_book = response.json()
    
    # Update it
    updated_data = test_book.copy()
    updated_data["title"] = "Updated Title"
    response = authorized_client.put(
        f"/api/v1/books/{created_book['id']}", 
        json=updated_data
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_delete_book(authorized_client, test_book):
    # First create a book
    response = authorized_client.post("/api/v1/books/", json=test_book)
    created_book = response.json()
    
    # Delete it
    response = authorized_client.delete(f"/api/v1/books/{created_book['id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"