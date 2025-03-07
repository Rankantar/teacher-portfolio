from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from .database import engine, SessionLocal
from .models import Base, Course, Student
from .api.api import api_router

app = FastAPI(title="Teacher Portfolio API")

# Include API router
app.include_router(api_router)

# Event to create tables on startup if they don't exist
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    
    # Check if we need to seed initial data
    db = SessionLocal()
    try:
        course_count = db.query(Course).count()
        student_count = db.query(Student).count()
        
        # Seed initial course data if no courses exist
        if course_count == 0:
            initial_courses = [
                {"course_name": "Infi 1"},
                {"course_name": "Infi 2"},
                {"course_name": "Linear Algebra"},
                {"course_name": "ODE"},
                {"course_name": "PDE"},
                {"course_name": "Mechanics"},
                {"course_name": "Electricity and Magnetism"},
                {"course_name": "Modern Physics"},
                {"course_name": "Waves"},
                {"course_name": "Quantum Mechanics"}
            ]
            for i, course_data in enumerate(initial_courses, 1):
                course = Course(course_id=i, **course_data)
                db.add(course)
        
        # Seed initial student data if no students exist
        if student_count == 0:
            initial_students = [
                {"student_name": "Orr Ox", "hours": 50},
                {"student_name": "Ran Chuck", "hours": 2},
                {"student_name": "Suli-Mani", "hours": 5}
            ]
            for i, student_data in enumerate(initial_students, 1):
                student = Student(student_id=i, **student_data)
                db.add(student)
        
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error seeding database: {str(e)}")
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"} 