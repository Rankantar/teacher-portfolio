#todo: data base, security protocols, schedule, email notification, translate
from fastapi import FastAPI

app = FastAPI()

courses = [#TODO add descriptions and headlines?
    {'course_id': 1, 'course_name': 'חדו"א 1',
     'description': 'סדרות\n חקירת פונקציות בעלות נעלם אחד\n טורים'},
    {'course_id': 2, 'course_name': 'חדו"א 2'},
    {'course_id': 3, 'course_name': 'אלגברה לינארית'},
    {'course_id': 4, 'course_name': 'משוואות דיפרנציאליות רגילות'},
    {'course_id': 5, 'course_name': 'מכניקה קלאסית',
     'description': 'א. קינמטיקה בקואורדינאטות קרטזיות ובקואורדינאטות פולאריות.\n'
                    'ב. חוקי ניוטון ותנועת חלקיק נקודתי. פתרון בעיות עם גרביטציה, חיכוך, קפיצים, גלגלות ותנועת מטוטלת.\n'
                    'ג. תנע קווי ומתקף. בעיות מכניקה עם פליטת או קליטת מסה.\n'
                    'ד. משפט עבודה ואנרגיה. התנגשויות אלסטיות ואיבוד אנרגיה.\n'
                    'ה. תנע זוויתי של חלקיק נקודתי. מומנט כוח (טורק). \n'
                    'ו. חוקי קפלר של תנועת הפלנטות ופיזור קלאסי.\n'
                    'ז. תנועת גוף קשיח, כאשר כיוון ציר הסיבוב קבוע במרחב. ממונט אינרציה. פתרון בעיות גלגול והחלקה.'},
    {'course_id': 6, 'course_name': 'חשמל ומגנטיות'},
    {'course_id': 7, 'course_name': 'פיזיקה מודרנית'},
    {'course_id': 8, 'course_name': 'גלים'},
    {'course_id': 9, 'course_name': 'מכניקה קוונטית 1'},
    {'course_id': 10, 'course_name': 'מתמטיקה לבגרות'},
    {'course_id': 11, 'course_name': 'פיזיקה לבגרות'}
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
