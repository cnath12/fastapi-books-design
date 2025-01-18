from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Books API",
        "version": "1.0.0"
    }

@router.get("/health/database")
async def database_health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1")).scalar()  
        return {
            "status": "healthy",
            "service": "database",
            "details": "Connection successful"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "database",
            "details": str(e)
        }