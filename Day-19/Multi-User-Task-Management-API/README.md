# Multi-User Task Management API

## Description

This project is a simple API that allows registered users to create and manage their own tasks.

## Objective

The objective is to practice authentication, authorization, database relationships, API development, and input validation with FastAPI.

## Tools Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Password hashing with `pwdlib`

## Project Structure

```text
Multi-User-Task-Management-API/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── requirements.txt
├── README.md
└── sample_output.txt
```

## Features

- User registration
- Password hashing
- Token-based login
- Protected task endpoints
- Create, view, update, and delete tasks
- User-specific task access
- SQLite database storage
- Automatic Swagger/OpenAPI documentation
- Request validation with Pydantic

## Database Models

The `User` model contains `id`, `username`, `email`, and `hashed_password`.

The `Task` model contains `id`, `title`, `description`, `completed`, and `owner_id`.

Each task belongs to one user through the `owner_id` foreign key. The SQLAlchemy relationship also allows a user to have multiple tasks.

## Authentication

A user registers with a username, email, and password. The password is hashed before it is stored in SQLite. During login, the API verifies the password and returns a bearer token.

Send the token in the header of protected requests:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Authorization

Every task query uses the authenticated user's ID. A user can only list, view, update, or delete tasks where `owner_id` matches their own ID. Trying to access another user's task returns `404 Not Found` with a clear error message.

## API Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/` | Check that the API is running | No |
| POST | `/register` | Register a new user | No |
| POST | `/login` | Log in and receive a token | No |
| POST | `/tasks` | Create a task | Yes |
| GET | `/tasks` | View the current user's tasks | Yes |
| GET | `/tasks/{task_id}` | View one owned task | Yes |
| PUT | `/tasks/{task_id}` | Update one owned task | Yes |
| DELETE | `/tasks/{task_id}` | Delete one owned task | Yes |

## Validation

Pydantic schemas validate username, password, title, description, and completed values. The API returns validation errors for invalid request data and appropriate HTTP status codes for invalid authentication, duplicate users, and missing tasks.

## Installation

Open this project folder and install the requirements:

```text
pip install -r requirements.txt
```

## Run the API

```text
uvicorn main:app --reload
```

The SQLite database file `tasks.db` is created automatically when the application starts.

## Swagger Documentation

Open the automatic documentation in a browser:

```text
http://127.0.0.1:8000/docs
```

The OpenAPI specification is also available at `/openapi.json`.

## Sample API Usage

Register a user:

```text
POST /register
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "secret123"
}
```

Log in:

```text
POST /login
{
  "username": "alice",
  "password": "secret123"
}
```

Create a task with the returned bearer token:

```text
POST /tasks
{
  "title": "Learn FastAPI",
  "description": "Practice protected endpoints"
}
```

## Sample Output

See `sample_output.txt` for successful API test results, including an authorization check using a second user and invalid authentication cases.

## Concepts Learned

- FastAPI routes and dependencies
- SQLAlchemy models and relationships
- SQLite database operations
- Password hashing
- Bearer token authentication
- User-specific authorization
- Pydantic validation
- HTTP status codes
- Swagger/OpenAPI documentation

## Conclusion

This task demonstrates how to build a small multi-user API where authentication and database ownership rules work together to protect user data.
