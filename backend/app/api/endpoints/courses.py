from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...database import get_db
from ... import crud, schemas

router = APIRouter()

@router.get('/', response_model=List[schemas.CourseModel])
async def courses_info(db: Session = Depends(get_db)):
    courses = crud.get_courses(db)
    return courses

@router.get('/{course_id}', response_model=schemas.CourseModel)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post('/', response_model=schemas.CourseModel)
async def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, course) 