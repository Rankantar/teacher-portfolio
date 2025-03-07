#todo: data base, security protocols, schedule, email notification, translate
# from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_FILE", "totemic-audio-453015-j5-c7d6d598d32c.json")

# Initialize the Google Calendar API client
try:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('calendar', 'v3', credentials=credentials)
except Exception as e:
    logger.error("Failed to initialize Google Calendar service: %s", e)
    raise

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

@app.post("/create_event")
async def create_event(event: CalendarEvent):
    calendar_id = 'primary'  # Use 'primary' or your specific calendar ID
    try:
        event_data = event.dict(exclude_unset=True)
        created_event = service.events().insert(calendarId=calendar_id, body=event_data).execute()
        return {"event_id": created_event.get('id')}
    except Exception as e:
        logger.error("Error creating event: %s", e)
        raise HTTPException(status_code=500, detail="Error creating event")

courses = [#TODO add descriptions and headlines?
    {'course_id': 1, 'course_name': 'חדו"א 1',
     'description': 'סדרות\n חקירת פונקציות בעלות נעלם אחד\n טורים'},
    {'course_id': 2, 'course_name': 'חדו"א 2'},
    {'course_id': 3, 'course_name': 'אלגברה לינארית'},
    {'course_id': 4, 'course_name': 'משוואות דיפרנציאליות רגילות'},
    {'course_id': 5, 'course_name': 'מכניקה קלאסית',
     'description': 'א. קינמטיקה.\n'
                    'ב. חוקי ניוטון.\n'
                    'ג. תנע קווי ומתקף.\n'
                    'ד. משפט עבודה ואנרגיה.\n'
                    'ה. תנע זוויתי ומומנט כוח (טורק).\n'
                    'ו. חוקי קפלר\n'
                    'ז. תנועת גוף קשיח.'},
    {'course_id': 6, 'course_name': 'חשמל ומגנטיות',
     'description': 'א. אלקטרוסטטיקה.\n'
                    'ב. מעגלים חשמליים.\n'
                    'ג. שדה מגנטי.'},
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
