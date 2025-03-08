from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String
from .database import Base

class Course(Base):
    __tablename__ = "courses"
    
    course_id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, index=True)
    description = Column(String, index = False)
    difficulty = Column(String, index = False)

class Student(Base):
    __tablename__ = "students"
    
    student_id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, index=True)
    hours = Column(Integer) 

# Define a Pydantic model for the calendar event
class CalendarEvent(BaseModel):
    summary: str
    location: str = None
    description: str = None
    start: dict = Field(
        ...,
        example={"dateTime": "2023-03-24T10:00:00-07:00", "timeZone": "America/Los_Angeles"}
    )
    end: dict = Field(
        ...,
        example={"dateTime": "2023-03-24T11:00:00-07:00", "timeZone": "America/Los_Angeles"}
    )
    attendees: list = None
    reminders: dict = None