from fastapi import APIRouter, HTTPException
from google.oauth2 import service_account
from app.models import CalendarEvent
from app.schemas import SlotTime
from datetime import datetime, timedelta
from googleapiclient.discovery import build
import os
import logging
import pytz

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

@router.get("/available_slots")
async def get_available_slots(date: datetime):
    """
    Retrieve available time slots for a specific date.
    Time slots are hourly from 10:00 to 18:00.
    
    Example: /available_slots?date=2023-03-24T00:00:00Z
    """
    # Set the timezone to the server's timezone or a specific one
    timezone = pytz.timezone('Asia/Jerusalem')  # Adjust to your preferred timezone
    
    # Create start and end datetime for the requested date
    start_date = datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=timezone)
    end_date = start_date + timedelta(days=1)
    
    # Get all events for the requested date
    calendar_id = 'primary'
    try:
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start_date.isoformat(),
            timeMax=end_date.isoformat(),
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = events_result.get('items', [])
        
        # Create hourly slots from 10:00 to 18:00
        available_slots = []
        for hour in range(10, 18):
            slot_start = datetime(date.year, date.month, date.day, hour, 0, 0, tzinfo=timezone)
            slot_end = slot_start + timedelta(hours=1)
            
            # Check if the slot overlaps with any existing event
            is_available = True
            for event in events:
                event_start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
                event_end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
                
                # Convert to the same timezone for comparison
                event_start = event_start.astimezone(timezone)
                event_end = event_end.astimezone(timezone)
                
                # Check for overlap
                if (slot_start < event_end and slot_end > event_start):
                    is_available = False
                    break
            
            # Add the slot to the list
            available_slots.append(
                SlotTime(
                    start_time=slot_start.isoformat(),
                    end_time=slot_end.isoformat(),
                    is_available=is_available
                )
            )
        
        return {"slots": available_slots}
    except Exception as e:
        logger.error("Error fetching available slots: %s", e)
        raise HTTPException(status_code=500, detail="Error fetching available slots")
