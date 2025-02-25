# FastAPI Books API

A comprehensive RESTful API for book management, built with FastAPI, featuring robust authentication, real-time updates, and advanced functionality.

## Features

- **Authentication**
  * JWT-based user authentication
  * Secure token management
  * Token refresh mechanism

- **Book Management**
  * Full CRUD operations for books
  * Pagination support
  * Detailed book information tracking

- **Real-Time Capabilities**
  * Server-Sent Events (SSE) for live updates
  * Instant notifications on book changes

- **Operational Excellence**
  * Health monitoring endpoints
  * Comprehensive API documentation
  * SQLite database with migration potential

## Prerequisites

- Python 3.11+
- pip (Python package manager)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/cnath12/fastapi-books-design.git
cd fastapi-books-design
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate

# On Unix or MacOS
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Generate a secret key
python generate_key.py

# Update .env with your secret key
```

## 🌐 Running the Application

```bash
# Start the server with auto-reload
uvicorn app.main:app --reload
```

### Access Points

- **API Root**: `http://localhost:8000/`
- **Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc Docs**: `http://localhost:8000/redoc`

## 📡 API Endpoints

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register` | POST | Register new user |
| `/api/v1/auth/login` | POST | Login and get token |
| `/api/v1/auth/refresh-token` | POST | Refresh JWT token |

### Books

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/books` | GET | List books (with pagination) |
| `/api/v1/books/{id}` | GET | Get specific book |
| `/api/v1/books` | POST | Create new book |
| `/api/v1/books/{id}` | PUT | Update book |
| `/api/v1/books/{id}` | DELETE | Delete book |
| `/api/v1/books/stream` | GET | SSE endpoint for real-time updates |

### Health Monitoring

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | API health check |
| `/api/v1/health/database` | GET | Database health check |

## 🧪 Testing

```bash
# Run test suite
pytest
```

## Deployment

Deployed on Heroku: 
https://fastapi-books-api-a676a812e510.herokuapp.com/

### Local to Heroku Deployment

```bash
# Install Heroku CLI and login
heroku create fastapi-books-api

# Configure environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set API_V1_STR="/api/v1"
heroku config:set PROJECT_NAME="Books API"
heroku config:set ACCESS_TOKEN_EXPIRE_DAYS=7

# Deploy
git push heroku main
```


### 5. Database Setup

#### Option A: Use Included Sample Database
This repository includes a pre-populated SQLite database (`app/db/books.db`) with 500 sample books for immediate testing and development. The database is located at:
fastapi-books-design/
└── app/
└── db/
└── books.db

The sample database is included for ease of getting started and development purposes.

## Future Enhancements

### 1. Database Improvements
- Implement Alembic migrations for schema management
- Migration to PostgreSQL for production scaling
- Database seeding scripts and data validation
- Backup and restore procedures
- Encrypted connections and security audits
- Connection pooling for concurrent access

### 2. Authentication & Security
- Email verification system
- Password reset functionality
- Role-based access control (RBAC)
- Enhanced access control mechanisms
- Regular security audits

### 3. API Features & Performance
- Advanced search and filtering capabilities
- Bulk operations support
- Rate limiting implementation
- API versioning
- Performance monitoring and optimization
- Caching mechanisms

### 4. Developer Experience
- Comprehensive API documentation
- Integration test suite expansion
- CI/CD pipeline improvements
- Development environment containerization
- API client SDK generation