from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager

from .database import engine, SessionLocal
from .models import Base, Course, Student
from .api.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and seed data
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
                {'course_name': 'חדו"א 1',
                'description': 'א. גבולות של סדרות.\n'
                               'ב. גבולות של פונקציות.\n'
                               'ג. נגזרות.\n'
                               'ד. אינטגרלים.\n'
                               'ה. טורים אינסופיים והתכנסות טורים.',
                 'difficulty': 2},
                {'course_name': 'חדו"א 2',
                'description': 'א. פונקציות מרובות משתנים.\n'
                               'ב. נגזרות חלקיות.\n'
                               'ג. כופלי לגראנג.\n'
                               'ד. אינטגרלים של פונקציות מרובות משתנים.\n'
                               'ה. וקטורים ואופרטורים וקטוריים.\n'
                               'ו. טורי פורייה.',
                 'difficulty': 2},
                {'course_name': 'אלגברה לינארית',
                'description': 'א. מערכת משוואות לינארית.\n'
                               'ב. אלגברה של מטריצות.\n'
                               'ג. מרחבים וקטוריים סופיים: מימד, בסיס, תלות לינארית.\n'
                               'ד. מיפויים לינאריים.\n'
                               'ה. מרחבי מכפלה פנימית.\n'
                               'ו. אופרטורים לכסינים ולכסון מטריצות.',
                 'difficulty': 2},
                {'course_name': 'משוואות דיפרנציאליות רגילות',
                 'description': 'א. משוואות פרידות.\n'
                                'ב. מד"ר הומוגנית.\n'
                                'ג. מד"ר לינארית מסדר ראשון.\n'
                                'ד. משוואות מדוייקות.\n'
                                'ה. מד"ר לינארית מסדר גבוה.\n',
                 'difficulty': 2},
                {'course_name': 'מכניקה קלאסית',
                'description': 'א. קינמטיקה.\n'
                                'ב. חוקי ניוטון.\n'
                                'ג. תנע קווי ומתקף.\n'
                                'ד. משפט עבודה ואנרגיה.\n'
                                'ה. תנע זוויתי ומומנט כוח (טורק).\n'
                                'ו. חוקי קפלר.\n'
                                'ז. תנועת גוף קשיח.',
                 'difficulty': 2},
                {'course_name': 'חשמל ומגנטיות',
                'description': 'א. אלקטרוסטטיקה.\n'
                                'ב. מעגלים חשמליים.\n'
                                'ג. שדה מגנטי.',
                 'difficulty': 2},
                {'course_name': 'פיזיקה מודרנית',
                'description': 'א. יחסות פרטית.\n'
                                'ב. קרינת גוף שחור.\n'
                                'ג. האפקט הפוטואלקטרי.\n'
                               'ד. מודל בוהר.',
                 'difficulty': 2},
                {'course_name': 'גלים',
                'description': 'א. משוואת הגלים.\n'
                                'ב. גלים עומדים.\n'
                                'ג. מעבר תווך.\n'
                               'ד. גלים ב2 ו3 מימדים.\n'
                               'ה. אפקט דופלר ופעימות.',
                 'difficulty': 3},
                {'course_name': 'מכניקה קוונטית 1',
                 'difficulty': 3},
                {'course_name': 'מתמטיקה לבגרות',
                 'description': 'א. 3 יחידות.\n'
                                'ב. 4 יחידות.\n'
                                'ג. 5 יחידות.',
                 'difficulty': 1},
                {'course_name': 'פיזיקה לבגרות',
                 'description': 'א. מכניקה.\n'
                                'ב. אלקטרומגנטיות.\n'
                                'ג. קרינה וחומר.',
                 'difficulty': 1}
            ]
            for i, course_data in enumerate(initial_courses, 1):
                # Extract only valid fields for the Course model (course_id and course_name)
                course_name = course_data.get('course_name', '')
                description = course_data.get('description', '')
                difficulty = course_data.get('difficulty', '')
                course = Course(course_id=i, course_name=course_name, description=description, difficulty=difficulty)
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
    
    yield  # This is where the app runs
    
    # Shutdown: Add any cleanup code here if needed

app = FastAPI(title="Teacher Portfolio API", lifespan=lifespan)

# Include API router
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Hello World"} 