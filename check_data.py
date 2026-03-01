from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def check_data():
    """
    Connects to the PostgreSQL database and prints the contents of the students,
    courses, and enrollment tables.
    """
    if not DATABASE_URL:
        print("DATABASE_URL not found in .env")
        return

    try:
        # Create engine and connect
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            print("\n" + "=" * 30)
            print("DATABASE INSPECTION REPORT")
            print("=" * 30)

            # Check Students
            print("\n--- Students Table ---")
            students = connection.execute(text("SELECT * FROM students")).fetchall()
            if not students:
                print("No students found.")
            else:
                for s in students:
                    print(
                        f"ID: {s.id} | Name: {s.name} | Email: {s.email} | Major: {s.major}"
                    )

            # Check Courses
            print("\n--- Courses Table ---")
            courses = connection.execute(text("SELECT * FROM courses")).fetchall()
            if not courses:
                print("No courses found.")
            else:
                for c in courses:
                    print(f"ID: {c.id} | Title: {c.title} | Credits: {c.credits}")

            # Check Enrollments
            print("\n--- Student-Course Enrollments (student_course) ---")
            enrollments = connection.execute(
                text("SELECT * FROM student_course")
            ).fetchall()
            if not enrollments:
                print("No enrollments found.")
            else:
                for e in enrollments:
                    print(f"Student ID: {e.student_id} | Course ID: {e.course_id}")

            print("\n" + "=" * 30)

    except Exception as e:
        print(f"Error connecting to or querying database: {e}")


if __name__ == "__main__":
    check_data()
