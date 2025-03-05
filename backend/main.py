#todo: data base, security protocols, schedule, email notification
from fastapi import FastAPI

app = FastAPI()


courses = [
    {'course_id': 1, 'course_name': 'Infi 1'},
    {'course_id': 2, 'course_name': 'Infi 2'},
    {'course_id': 3, 'course_name': 'Linear Algebra'},
    {'course_id': 4, 'course_name': 'ODE'},
    {'course_id': 5, 'course_name': 'PDE'},
    {'course_id': 6, 'course_name': 'Mechanics'},
    {'course_id': 7, 'course_name': 'Electricity and Magnetism'},
    {'course_id': 8, 'course_name': 'Modern Physics'},
    {'course_id': 9, 'course_name': 'Waves'},
    {'course_id': 10, 'course_name': 'Quantum Mechanics'}
]

students = [
    {'student_id': 1, 'student_name': 'Orr Ox', 'hours': 50},
    {'student_id': 2, 'student_name': 'Ran Chuck', 'hours': 2},
    {'student_id': 3, 'student_name': 'Suli-Mani', 'hours': 5},
]

@app.get('/courses')
async def courses_info():
    return courses

@app.get('/students')
async def students_info_fist_n(first_n: int  = None):
    if first_n:
        return students[:first_n]
    else:
        return students

# @app.get('/students')
# async def students_info_last_n(last_n: int  = None):
#     if last_n:
#         return students[last_n:]
#     else:
#         return students

@app.get("/")
async def root():
    return {"message": "Hello World"}