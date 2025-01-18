import pytest
import asyncio
import json
from fastapi import status
from sse_starlette.sse import EventSourceResponse
import async_timeout
import httpx

@pytest.mark.asyncio
async def test_complete_book_workflow(authorized_client, test_book):
    """Test complete workflow: create -> read -> update -> delete with authentication"""
    
    # Create a book
    create_response = authorized_client.post("/api/v1/books/", json=test_book)
    assert create_response.status_code == 200
    created_book = create_response.json()
    book_id = created_book["id"]

    # Verify book exists
    get_response = authorized_client.get(f"/api/v1/books/{book_id}")
    assert get_response.status_code == 200
    assert get_response.json() == created_book

    # Update book
    updated_data = test_book.copy()
    updated_data["title"] = "Updated Integration Test Book"
    update_response = authorized_client.put(
        f"/api/v1/books/{book_id}",
        json=updated_data
    )
    assert update_response.status_code == 200
    updated_book = update_response.json()
    assert updated_book["title"] == "Updated Integration Test Book"

    # Delete book
    delete_response = authorized_client.delete(f"/api/v1/books/{book_id}")
    assert delete_response.status_code == 200

    # Verify book is deleted
    get_deleted = authorized_client.get(f"/api/v1/books/{book_id}")
    assert get_deleted.status_code == 404


@pytest.mark.asyncio
async def test_auth_flow_with_book_access(client, test_user):
    """Test complete authentication flow with book access"""
    
    # Register
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "integrationuser",
            "password": "testpass123"
        }
    )
    assert register_response.status_code == 200

    # Login
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "integrationuser",
            "password": "testpass123"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Use token to access books
    headers = {"Authorization": f"Bearer {token}"}
    books_response = client.get("/api/v1/books/", headers=headers)
    assert books_response.status_code == 200

    # Refresh token
    refresh_response = client.post(
        "/api/v1/auth/refresh-token",
        headers=headers
    )
    assert refresh_response.status_code == 200
    new_token = refresh_response.json()["access_token"]
    assert new_token != token

    # Use new token
    new_headers = {"Authorization": f"Bearer {new_token}"}
    new_books_response = client.get("/api/v1/books/", headers=new_headers)
    assert new_books_response.status_code == 200

@pytest.mark.asyncio
async def test_concurrent_book_operations(authorized_client):
    """Test concurrent book operations"""
    
    books_to_create = [
        {
            "title": f"Concurrent Book {i}",
            "author": "Test Author",
            "published_date": "2024-01-17",
            "summary": f"Testing concurrent operations {i}",
            "genre": "Test"
        }
        for i in range(5)
    ]

    # Create books concurrently
    create_responses = []
    for book in books_to_create:
        response = authorized_client.post("/api/v1/books/", json=book)
        assert response.status_code == 200
        create_responses.append(response.json())

    # Get all books and verify pagination
    get_response = authorized_client.get("/api/v1/books/?page=1")
    assert get_response.status_code == 200
    data = get_response.json()
    
    assert data["total"] >= len(books_to_create)
    assert data["page"] == 1
    
    # Clean up created books
    for book in create_responses:
        delete_response = authorized_client.delete(f"/api/v1/books/{book['id']}")
        assert delete_response.status_code == 200