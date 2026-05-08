# Student Management API

FastAPI service for managing students, courses, grades, authentication, and summary reports. The project uses SQLAlchemy, Alembic, PostgreSQL, bearer-token authentication, pagination, lightweight caching, background jobs, rate limiting, and automated tests.

## Overview

- Student and course CRUD endpoints
- Grade management tied to student-course enrollments
- Bearer-token authentication with registration and login
- Paginated list endpoints with total counts
- Read-through caching on list and detail endpoints
- Background summary report generation
- Rate limiting middleware for request protection
- Alembic migrations and pytest-based test coverage

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pytest

## Project Structure

```text
student-management-api/
├── alembic/
├── app/
│   ├── crud/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── cache.py
│   ├── database.py
│   ├── main.py
│   ├── rate_limiter.py
│   └── reports.py
├── tests/
│   ├── integration/
│   └── unit/
├── .github/workflows/
├── alembic.ini
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository and enter the project directory.

```bash
git clone https://github.com/chiemeriev561-coder/student-management-api.git
cd student-management-api
```

2. Create and activate a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Create a `.env` file.

```env
DATABASE_URL=postgresql://user:password@localhost:5432/student_management
AUTH_SECRET_KEY=replace-this-with-a-long-random-secret
AUTH_TOKEN_EXPIRE_MINUTES=60
RATE_LIMIT_MAX_REQUESTS=60
RATE_LIMIT_WINDOW_SECONDS=60
```

5. Apply database migrations.

```bash
alembic upgrade head
```

6. Start the server.

```bash
uvicorn app.main:app --reload
```

Useful URLs:

- API root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Usage

### Authentication Flow

This API uses signed bearer tokens. It does not use OAuth, and the token format is not JWT. Clients should:

1. Register or log in.
2. Copy the returned `access_token`.
3. Send it on protected routes as:

```http
Authorization: Bearer <access_token>
```

### Example: Register

Request:

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "strong-password"
  }'
```

Response:

```json
{
  "access_token": "token-value",
  "token_type": "bearer",
  "expires_at": "2026-05-09T11:30:00Z",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  }
}
```

### Example: Create Student

Request:

```bash
curl -X POST http://127.0.0.1:8000/students/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "age": 21,
    "email": "alice@example.com",
    "major": "Computer Science"
  }'
```

Response:

```json
{
  "id": 1,
  "name": "Alice Johnson",
  "age": 21,
  "email": "alice@example.com",
  "major": "Computer Science"
}
```

### Example: List Students With Pagination

Request:

```bash
curl -X GET "http://127.0.0.1:8000/students/?skip=0&limit=20" \
  -H "Authorization: Bearer <access_token>"
```

Response:

```json
{
  "items": [
    {
      "id": 1,
      "name": "Alice Johnson",
      "age": 21,
      "email": "alice@example.com",
      "major": "Computer Science"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 20
}
```

## Endpoint Reference

### Root

`GET /`

- Description: Health-style welcome endpoint
- Authentication: Not required
- Success response: `200 OK`

Example response:

```json
{
  "message": "Welcome to the Student Management API!"
}
```

### Authentication

`POST /auth/register`

- Description: Create a user account and issue an access token
- Authentication: Not required
- Request body:

```json
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "strong-password"
}
```

- Success response: `201 Created`
- Error codes:
  - `400 Bad Request` when username already exists
  - `400 Bad Request` when email already exists

`POST /auth/login`

- Description: Authenticate a user and issue an access token
- Authentication: Not required
- Request body:

```json
{
  "username": "admin",
  "password": "strong-password"
}
```

- Success response: `200 OK`
- Error codes:
  - `401 Unauthorized` for invalid credentials

### Students

`GET /students/`

- Description: Paginated student list
- Authentication: Required
- Query parameters:
  - `skip` default `0`
  - `limit` default `20`, max `100`
- Success response: `200 OK`
- Headers:
  - `X-Cache: HIT|MISS`
- Error codes:
  - `401 Unauthorized` for missing or invalid token
  - `422 Unprocessable Entity` for invalid pagination values

`GET /students/{student_id}`

- Description: Fetch one student by id
- Authentication: Required
- Path parameters:
  - `student_id` integer
- Success response: `200 OK`
- Headers:
  - `X-Cache: HIT|MISS`
- Error codes:
  - `401 Unauthorized`
  - `404 Not Found` when student does not exist

`POST /students/`

- Description: Create a student
- Authentication: Required
- Request body:

```json
{
  "name": "Alice Johnson",
  "age": 21,
  "email": "alice@example.com",
  "major": "Computer Science"
}
```

- Success response: `200 OK`
- Error codes:
  - `400 Bad Request` when email already exists
  - `401 Unauthorized`

`PUT /students/{student_id}`

- Description: Update one or more student fields
- Authentication: Required
- Success response: `200 OK`
- Error codes:
  - `401 Unauthorized`
  - `404 Not Found`

`DELETE /students/{student_id}`

- Description: Delete a student
- Authentication: Required
- Success response: `200 OK`
- Error codes:
  - `401 Unauthorized`
  - `404 Not Found`

### Courses

`GET /courses/`

- Description: Paginated course list
- Authentication: Required
- Query parameters:
  - `skip` default `0`
  - `limit` default `20`, max `100`
- Success response: `200 OK`
- Headers:
  - `X-Cache: HIT|MISS`
- Error codes:
  - `401 Unauthorized`
  - `422 Unprocessable Entity`

`GET /courses/{course_id}`

- Description: Fetch one course by id
- Authentication: Required
- Success response: `200 OK`
- Error codes:
  - `401 Unauthorized`
  - `404 Not Found`

`POST /courses/`

- Description: Create a course
- Authentication: Required
- Request body:

```json
{
  "title": "Algorithms",
  "description": "Core algorithms and analysis",
  "credits": 3
}
```

- Success response: `200 OK`
- Error codes:
  - `401 Unauthorized`

`PUT /courses/{course_id}`

- Description: Update one or more course fields
- Authentication: Required
- Success response: `200 OK`
- Error codes:
  - `401 Unauthorized`
  - `404 Not Found`

`DELETE /courses/{course_id}`

- Description: Delete a course
- Authentication: Required
- Success response: `200 OK`
- Error codes:
  - `401 Unauthorized`
  - `404 Not Found`

### Grades

`GET /grades/`

- Description: Paginated grade list across student-course enrollments
- Authentication: Required
- Query parameters:
  - `skip` default `0`
  - `limit` default `20`, max `100`
- Success response: `200 OK`
- Error codes:
  - `401 Unauthorized`

`GET /grades/{student_id}/{course_id}`

- Description: Fetch one grade record for a student-course pair
- Authentication: Required
- Success response: `200 OK`
- Error codes:
  - `401 Unauthorized`
  - `404 Not Found`

`POST /grades/`

- Description: Create a grade record for an existing student and course
- Authentication: Required
- Request body:

```json
{
  "student_id": 1,
  "course_id": 1,
  "grade": "A"
}
```

- Success response: `200 OK`
- Error codes:
  - `401 Unauthorized`
  - `404 Not Found` when student or course does not exist
  - `400 Bad Request` when the grade record already exists

`PUT /grades/{student_id}/{course_id}`

- Description: Update the grade for an existing student-course pair
- Authentication: Required
- Request body:

```json
{
  "grade": "A-"
}
```

- Success response: `200 OK`
- Error codes:
  - `401 Unauthorized`
  - `404 Not Found`

`DELETE /grades/{student_id}/{course_id}`

- Description: Delete a grade record
- Authentication: Required
- Success response: `200 OK`
- Error codes:
  - `401 Unauthorized`
  - `404 Not Found`

### Reports

`POST /reports/summary`

- Description: Queue a background summary report job
- Authentication: Required
- Success response: `202 Accepted`

Example response:

```json
{
  "job_id": "8a7cf0ef-8f7e-469a-a5a6-8dc03d799f4d",
  "status": "pending"
}
```

`GET /reports/summary/{job_id}`

- Description: Fetch the status or result of a report job
- Authentication: Required
- Success response: `200 OK`
- Error codes:
  - `401 Unauthorized`
  - `404 Not Found` when the job id is unknown

Example completed response:

```json
{
  "job_id": "8a7cf0ef-8f7e-469a-a5a6-8dc03d799f4d",
  "status": "completed",
  "created_at": "2026-05-09T10:00:00Z",
  "completed_at": "2026-05-09T10:00:01Z",
  "result": {
    "students": 1,
    "courses": 1,
    "enrollments": 0
  }
}
```

## Performance and Scalability Notes

- Pagination prevents unbounded list responses.
- A short-lived in-process cache reduces repeated read pressure on the database.
- Report generation runs in a background task instead of blocking the request thread.
- Enrollment lookup indexes are managed through Alembic migrations.
- Rate limiting protects the API from burst abuse.

## Testing

Run the full suite:

```bash
python -m pytest -q
```

Run specific layers:

```bash
python -m pytest tests/unit -q
python -m pytest tests/integration -q
```

The CI workflow in `.github/workflows/tests.yml` runs the suite on pushes and pull requests.

## Contributing

See [CONTRIBUTING.md](/home/victor/Documents/student-management-api/CONTRIBUTING.md:1). Short version:

- Create a branch from `main`
- Keep changes focused
- Run `python -m pytest -q`
- Add or update tests for behavior changes
- Generate Alembic migrations for schema changes
- Open a pull request with a clear summary

## License

This project is licensed under the MIT License.
