from fastapi import APIRouter

from app.api.endpoints import schedule, courses, students, prices

api_router = APIRouter()

api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(prices.router, prefix="/prices", tags=["prices"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])