from sqlalchemy.orm import Session
from . import models, schemas

# Course CRUD operations
def get_courses(db: Session):
    return db.query(models.Course).all()

def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.course_id == course_id).first()

def create_course(db: Session, course: schemas.CourseCreate):
    last_course = db.query(models.Course).order_by(models.Course.course_id.desc()).first()
    next_id = 1 if last_course is None else last_course.course_id + 1
    db_course = models.Course(course_id=next_id, course_name=course.course_name)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

# Student CRUD operations
def get_students(db: Session, first_n: int = None):
    query = db.query(models.Student)
    if first_n:
        return query.limit(first_n).all()
    return query.all()

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.student_id == student_id).first()

def create_student(db: Session, student: schemas.StudentCreate):
    last_student = db.query(models.Student).order_by(models.Student.student_id.desc()).first()
    next_id = 1 if last_student is None else last_student.student_id + 1
    db_student = models.Student(student_id=next_id, student_name=student.student_name, hours=student.hours)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student 