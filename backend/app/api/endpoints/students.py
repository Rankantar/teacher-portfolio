from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ...database import get_db
from ... import crud, schemas

router = APIRouter()

@router.get('/', response_model=List[schemas.StudentModel])
async def students_info(first_n: Optional[int] = None, db: Session = Depends(get_db)):
    students = crud.get_students(db, first_n)
    return students

@router.get('/{student_id}', response_model=schemas.StudentModel)
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post('/', response_model=schemas.StudentModel)
async def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student) 