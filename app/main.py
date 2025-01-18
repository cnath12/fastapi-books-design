from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import engine, Base
from app.api.v1.endpoints import auth, books, health
from app.core.errors import http_exception_handler

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    # 📚 Books API Documentation
    
    A comprehensive RESTful API for book management with authentication and real-time updates.
    
    ## Key Features
    * **🔐 Authentication**: JWT-based authentication with refresh mechanism
    * **📖 Books Management**: Complete CRUD operations with pagination
    * **🔄 Real-time Updates**: Server-Sent Events for live notifications
    * **🏥 Health Checks**: API and database monitoring
    
    ## Authentication
    All protected endpoints require a Bearer token:
    1. Register a new user (`/auth/register`)
    2. Login to get your token (`/auth/login`)
    3. Use the token in the Authorize button above ⬆️
    4. Refresh token when needed (`/auth/refresh-token`)
    
    ## Pagination
    Book listing supports pagination:
    - Default page size: 50 items
    - Use `page` parameter to navigate
    - Response includes total count and pages
    """,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Add error handlers
app.add_exception_handler(HTTPException, http_exception_handler)

# Include routers
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["auth"],
    responses={401: {"description": "Unauthorized"}}
)

app.include_router(
    books.router,
    prefix=f"{settings.API_V1_STR}/books",
    tags=["books"],
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Book not found"}
    }
)

app.include_router(
    health.router,
    prefix=f"{settings.API_V1_STR}",
    tags=["health"]
)

@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to the Books API",
        "docs": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": f"{settings.API_V1_STR}/openapi.json"
        }
    }
