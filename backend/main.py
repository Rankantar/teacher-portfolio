#todo: security protocols, schedule, email notification
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from pydantic import BaseModel

# Database URL from environment variables with default fallback
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/teacher_db")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database Models
class Course(Base):
    __tablename__ = "courses"
    
    course_id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, index=True)

class Student(Base):
    __tablename__ = "students"
    
    student_id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, index=True)
    hours = Column(Integer)

# Pydantic models for API
class CourseBase(BaseModel):
    course_name: str

class CourseCreate(CourseBase):
    pass

class CourseModel(CourseBase):
    course_id: int
    
    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    student_name: str
    hours: int

class StudentCreate(StudentBase):
    pass

class StudentModel(StudentBase):
    student_id: int
    
    class Config:
        orm_mode = True

app = FastAPI()

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

@app.get('/courses', response_model=List[CourseModel])
async def courses_info(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses

@app.get('/courses/{course_id}', response_model=CourseModel)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.post('/courses', response_model=CourseModel)
async def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    last_course = db.query(Course).order_by(Course.course_id.desc()).first()
    next_id = 1 if last_course is None else last_course.course_id + 1
    db_course = Course(course_id=next_id, course_name=course.course_name)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.get('/students', response_model=List[StudentModel])
async def students_info(first_n: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Student)
    if first_n:
        students = query.limit(first_n).all()
    else:
        students = query.all()
    return students

@app.get('/students/{student_id}', response_model=StudentModel)
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post('/students', response_model=StudentModel)
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    last_student = db.query(Student).order_by(Student.student_id.desc()).first()
    next_id = 1 if last_student is None else last_student.student_id + 1
    db_student = Student(student_id=next_id, student_name=student.student_name, hours=student.hours)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/")
async def root():
    return {"message": "Hello World"}
