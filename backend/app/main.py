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
                #TODO add descriptions and headlines?
                {'course_id': 1, 'course_name': 'חדו"א 1',
                'description': 'סדרות\n חקירת פונקציות בעלות נעלם אחד\n טורים'},
                {'course_id': 2, 'course_name': 'חדו"א 2'},
                {'course_id': 3, 'course_name': 'אלגברה לינארית'},
                {'course_id': 4, 'course_name': 'משוואות דיפרנציאליות רגילות'},
                {'course_id': 5, 'course_name': 'מכניקה קלאסית',
                'description': 'א. קינמטיקה.\n'
                                'ב. חוקי ניוטון.\n'
                                'ג. תנע קווי ומתקף.\n'
                                'ד. משפט עבודה ואנרגיה.\n'
                                'ה. תנע זוויתי ומומנט כוח (טורק).\n'
                                'ו. חוקי קפלר\n'
                                'ז. תנועת גוף קשיח.'},
                {'course_id': 6, 'course_name': 'חשמל ומגנטיות',
                'description': 'א. אלקטרוסטטיקה.\n'
                                'ב. מעגלים חשמליים.\n'
                                'ג. שדה מגנטי.'},
                {'course_id': 7, 'course_name': 'פיזיקה מודרנית'},
                {'course_id': 8, 'course_name': 'גלים'},
                {'course_id': 9, 'course_name': 'מכניקה קוונטית 1'},
                {'course_id': 10, 'course_name': 'מתמטיקה לבגרות'},
                {'course_id': 11, 'course_name': 'פיזיקה לבגרות'}
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