from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db

router = APIRouter()

@router.get("/health",
   summary="Check API health",
   description="Check if the API service is running properly")
async def health_check():
   return {
       "status": "healthy",
       "service": "Books API", 
       "version": "1.0.0"
   }

@router.get("/health/database",
   summary="Check database health",
   description="Check if the database connection is working properly")
async def database_health_check(db: Session = Depends(get_db)):
   try:
       # Execute a simple query to check database connection
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