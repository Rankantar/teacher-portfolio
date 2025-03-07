from fastapi import APIRouter
from .endpoints import courses, students

api_router = APIRouter()

api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(students.router, prefix="/students", tags=["students"]) 