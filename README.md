
📘 Student Management API

A lightweight and efficient RESTful API for managing student records, built with FastAPI and SQLite. It provides endpoints for creating, retrieving, updating, and deleting student data, with a clean architecture suitable for learning, prototyping, or production‑ready extensions.

🚀 Features

CRUD operations for student records

FastAPI automatic interactive docs (Swagger & ReDoc)

SQLite database for simple, file‑based persistence

Pydantic models for validation

Modular project structure

Async‑ready architecture

🛠️ Tech Stack

FastAPI (Python)

SQLite

SQLAlchemy or Tortoise ORM (depending on your implementation)

Uvicorn (ASGI server)

Pydantic

📂 Project Structure

Adjust this to match your actual folders, but a typical layout looks like:

student-management-api/
│
├── app/
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── database.py
│   └── main.py
│
├── requirements.txt
└── README.md

⚙️ Installation & Setup

1. Clone the repository

git clone https://github.com/chiemeriev561-coder/student-management-api.git
cd student-management-api

2. Create a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. Install dependencies

pip install -r requirements.txt

4. Run the application

uvicorn app.main:app --reload

The API will be available at:http://127.0.0.1:8000

Interactive documentation:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

📡 API Endpoints

Students

Method

Endpoint

Description

GET

/students

Get all students

GET

/students/{id}

Get a single student

POST

/students

Create a new student

PUT

/students/{id}

Update a student

DELETE

/students/{id}

Delete a student

📝 Example Request (Create Student)

POST /students
{
  "name": "John Doe",
  "age": 20,
  "department": "Computer Science"
}

🗄️ Database

This project uses SQLite, a simple file‑based database.The database file (e.g., students.db) is automatically created on first run.

If you’re using SQLAlchemy, your connection string may look like:

sqlite:///./students.db

🧪 Running Tests (if applicable)

If you add tests later:

pytest

🤝 Contributing

Contributions are welcome.

Fork the repository

Create a feature branch

Commit your changes

Open a pull request

📄 License

This project is licensed under the MIT License.

If you want, I can refine this further to match your exact folder structure, models, or API routes.
