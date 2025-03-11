from fastapi import APIRouter, HTTPException
from google.oauth2 import service_account
from app.models import CalendarEvent
from datetime import datetime
from googleapiclient.discovery import build
import os
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

router = APIRouter()


@router.post("/create_event")
async def create_event(event: CalendarEvent):
    calendar_id = 'primary'  # Use 'primary' or your specific calendar ID
    try:
        event_data = event.dict(exclude_unset=True)
        created_event = service.events().insert(calendarId=calendar_id, body=event_data).execute()
        return {"event_id": created_event.get('id')}
    except Exception as e:
        logger.error("Error creating event: %s", e)
        raise HTTPException(status_code=500, detail="Error creating event")


@router.get("/get_events")
async def get_events(start: datetime, end: datetime):
    """
    Retrieve all events between the specified start and end time.
    The start and end query parameters should be in ISO 8601 format.
    
    Example: /get_events?start=2023-03-24T00:00:00Z&end=2023-03-25T00:00:00Z
    """
    calendar_id = 'primary'
    try:
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start.isoformat(),
            timeMax=end.isoformat(),
            singleEvents=True,  # Expands recurring events
            orderBy="startTime"
        ).execute()
        events = events_result.get('items', [])
        return {"events": events}
    except Exception as e:
        logger.error("Error fetching events: %s", e)
        raise HTTPException(status_code=500, detail="Error fetching events")
