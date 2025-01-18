from sqlalchemy import text

def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_database_health(client, db):  # Add db fixture
    # Ensure database is properly initialized
    db.execute(text("SELECT 1")).scalar()
    
    response = client.get("/api/v1/health/database")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "database"
    assert "details" in data