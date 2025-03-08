from pydantic import BaseModel

class CourseBase(BaseModel):
    course_name: str
    description: str
    difficulty: str

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