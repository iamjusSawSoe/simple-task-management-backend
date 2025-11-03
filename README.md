# Task Management API - Backend

A robust FastAPI backend for a task management application with JWT authentication, SQLAlchemy ORM, and comprehensive API documentation.

## 🚀 Features

- **JWT Authentication**: Secure user authentication with bcrypt password hashing
- **RESTful API**: Well-structured endpoints following REST conventions
- **SQLAlchemy ORM**: Efficient database operations with optimized queries
- **Pydantic Validation**: Request/response validation with type safety
- **Auto Documentation**: Interactive API docs via OpenAPI (Swagger UI)
- **Clean Architecture**: Separation of concerns with services, routes, and models
- **CORS Support**: Configured for frontend integration

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)

## 🛠️ Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd backend
```

2. **Create virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Unix/MacOS
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
cp .env.example .env
```

Edit `.env` file and update the values:

```env
DATABASE_URL=sqlite:///./task_management.db
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

⚠️ **Important**: Generate a secure SECRET_KEY in production:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🏃‍♂️ Running the Application

**Development mode with auto-reload:**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- Base URL: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📚 API Documentation

### Authentication Endpoints

#### Register User

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "John Doe",
  "password": "securepassword123"
}
```

#### Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Task Endpoints (Requires Authentication)

All task endpoints require the `Authorization` header:

```
Authorization: Bearer <your_access_token>
```

#### Get All Tasks

```http
GET /api/v1/tasks
GET /api/v1/tasks?status=pending
GET /api/v1/tasks?priority=high
GET /api/v1/tasks?status=in-progress&priority=medium
```

#### Get Single Task

```http
GET /api/v1/tasks/{task_id}
```

#### Create Task

```http
POST /api/v1/tasks
Content-Type: application/json

{
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API docs",
  "status": "pending",
  "priority": "high",
  "due_date": "2025-10-20T23:59:59"
}
```

#### Update Task

```http
PUT /api/v1/tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated title",
  "status": "in-progress",
  "priority": "medium"
}
```

#### Delete Task

```http
DELETE /api/v1/tasks/{task_id}
```

## 🗂️ Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py          # Authentication routes
│   │   │   └── tasks.py         # Task CRUD routes
│   │   └── dependencies.py      # Shared dependencies (auth)
│   ├── core/
│   │   ├── config.py            # Configuration & settings
│   │   └── security.py          # JWT & password hashing
│   ├── db/
│   │   └── database.py          # Database connection & session
│   ├── models/
│   │   ├── user.py              # User SQLAlchemy model
│   │   └── task.py              # Task SQLAlchemy model
│   ├── schemas/
│   │   ├── user.py              # User Pydantic schemas
│   │   └── task.py              # Task Pydantic schemas
│   ├── services/
│   │   ├── auth_service.py      # Authentication business logic
│   │   └── task_service.py      # Task business logic
│   └── main.py                  # FastAPI application entry point
├── requirements.txt
├── .env.example
└── README.md
```

## 🔐 Security Features

- **Password Hashing**: Bcrypt algorithm with automatic salting
- **JWT Tokens**: Secure token-based authentication
- **Token Expiration**: Configurable token lifetime
- **SQL Injection Protection**: SQLAlchemy ORM parameterized queries
- **CORS Configuration**: Controlled origin access

## 🎯 Key Design Decisions

### Architecture Choices

1. **Service Layer Pattern**: Business logic separated into service classes for better testability and maintainability
2. **Dependency Injection**: FastAPI's dependency injection for database sessions and authentication
3. **Schema Validation**: Pydantic models ensure data integrity at API boundaries
4. **Enum Types**: Type-safe status and priority values

### Database Optimization

- **Indexed Columns**: Email and task title for faster queries
- **Relationship Loading**: Configured for efficient data fetching
- **Filtered Queries**: Database-level filtering instead of in-memory filtering

### API Design

- **RESTful Conventions**: Proper HTTP methods and status codes
- **Versioned API**: `/api/v1` prefix for future compatibility
- **Comprehensive Docs**: Auto-generated OpenAPI documentation
- **Error Handling**: Consistent error responses with appropriate status codes

## 🧪 Testing the API

You can test the API using:

1. **Swagger UI** (Built-in): `http://localhost:8000/docs`
2. **cURL**:

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"Test User","password":"test123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Get tasks (use token from login)
curl -X GET http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

3. **Postman/Insomnia**: Import OpenAPI spec from `/docs`

## 📝 Assumptions Made

1. **Single Tenant**: Each user can only access their own tasks
2. **SQLite Database**: Suitable for development; switch to PostgreSQL/MySQL for production
3. **Token Storage**: Frontend handles token storage and management
4. **Date Format**: ISO 8601 format for date/time fields
5. **Task Ownership**: Tasks are always associated with the creator user

## 🚀 Production Considerations

Before deploying to production:

1. **Change SECRET_KEY**: Generate a strong random secret key
2. **Use Production Database**: Switch from SQLite to PostgreSQL/MySQL
3. **Enable HTTPS**: Use SSL/TLS certificates
4. **Environment Variables**: Use secure secret management
5. **Rate Limiting**: Implement API rate limiting
6. **Logging**: Add comprehensive logging for debugging
7. **Database Migrations**: Use Alembic for schema migrations

## 📞 Support

For questions or issues, contact: hr@horizonlabs.ai

## 📄 License

This project is created for technical assessment purposes.
