# 📘 Student Management API

A robust and scalable RESTful API built with **FastAPI**, designed for managing students and academic courses. This project features a clean modular architecture, automated database migrations, and production-ready configurations.

---

## 🚀 Key Features

- **Full CRUD Support**: Manage Students and Courses through intuitive endpoints.
- **Relational Data**: Many-to-Many relationships between students and courses (Database level).
- **Automated Migrations**: Schema versioning managed by **Alembic**.
- **Data Validation**: Strict type-checking and validation using **Pydantic v2**.
- **Interactive Documentation**: Instant API testing via Swagger UI and ReDoc.
- **Automated Testing**: Comprehensive test suite using **pytest** and an in-memory SQLite database.

---

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **Testing**: [pytest](https://docs.pytest.org/)

---

## 📂 Project Structure

```text
student-management-api/
├── alembic/              # Database migration scripts and environment
├── app/                  # Main application source code
│   ├── crud/             # Create, Read, Update, Delete logic
│   ├── models/           # SQLAlchemy database models
│   ├── routers/          # FastAPI route controllers
│   ├── schemas/          # Pydantic data validation schemas
│   ├── database.py       # DB connection and session management
│   └── main.py           # Application entry point
├── tests/                # Automated test suite
├── .env                  # Environment variables (DB_URL, etc.)
├── alembic.ini           # Alembic configuration
└── requirements.txt      # Project dependencies
```

---

## ⚙️ Installation & Setup

### 1. Clone & Prepare Environment
```bash
git clone https://github.com/chiemeriev561-coder/student-management-api.git
cd student-management-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/student_management
```

### 3. Run Migrations
Apply the latest schema to your database:
```bash
alembic upgrade head
```

### 4. Start the Server
```bash
uvicorn app.main:app --reload
```
- **API URL**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📡 API Reference

### Students
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/students/` | List students (paginated) |
| `GET` | `/students/{id}` | Retrieve a specific student |
| `POST` | `/students/` | Register a new student |
| `PUT` | `/students/{id}` | Update student details |
| `DELETE` | `/students/{id}` | Remove a student |

### Courses
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/courses/` | List courses (paginated) |
| `GET` | `/courses/{id}` | Retrieve a specific course |
| `POST` | `/courses/` | Create a new course |
| `PUT` | `/courses/{id}` | Update course information |
| `DELETE` | `/courses/{id}` | Remove a course |

---

## 🧪 Testing

The project uses `pytest` with a dedicated in-memory SQLite configuration to ensure isolation during tests.

```bash
pytest
```

---

## 🛠️ Development

### Database Migrations
When updating SQLAlchemy models, generate a new migration:
```bash
alembic revision --autogenerate -m "Describe your changes"
alembic upgrade head
```

---

## 📄 License
This project is licensed under the **MIT License**.
