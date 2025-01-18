from fastapi import FastAPI, HTTPException
from app.core.config import settings
from app.db.database import engine, Base
from app.api.v1.endpoints import auth, books, health
from app.core.errors import http_exception_handler

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Add error handlers
app.add_exception_handler(HTTPException, http_exception_handler)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(books.router, prefix=f"{settings.API_V1_STR}/books", tags=["books"])
app.include_router(health.router, prefix=f"{settings.API_V1_STR}", tags=["health"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Books API"}


# from fastapi import FastAPI
# from app.core.config import settings
# from app.db.database import engine, Base
# from app.api.v1.endpoints import auth, books  # Add books import

# # Create tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI(
#     title=settings.PROJECT_NAME,
#     openapi_url=f"{settings.API_V1_STR}/openapi.json"
# )

# # Include routers
# app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
# app.include_router(books.router, prefix=f"{settings.API_V1_STR}/books", tags=["books"])  # Add books router

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the Books API"}

# from fastapi import FastAPI
# from app.core.config import settings
# from app.db.database import engine, Base
# from app.api.v1.endpoints import auth

# # Create tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI(
#     title=settings.PROJECT_NAME,
#     openapi_url=f"{settings.API_V1_STR}/openapi.json"
# )

# # Include routers
# app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the Books API"}