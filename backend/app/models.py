from sqlalchemy import Column, Integer, String
from .database import Base

class Course(Base):
    __tablename__ = "courses"
    
    course_id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, index=True)

class Student(Base):
    __tablename__ = "students"
    
    student_id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, index=True)
    hours = Column(Integer) 