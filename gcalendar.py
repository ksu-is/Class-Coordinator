 import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os


# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

file_path=''

def get_calendar_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def add_calendar_event(assignment_title,assignment_date):
    service = get_calendar_service()

    # Call the Calendar API
    event = {
        'summary': assignment_title,
        'location': 'KSU',
        'description': 'Class',
        'start': {
            'date': assignment_date,
            'timeZone': 'America/New_York',
        },
        'end': {
            'date': assignment_date,
            'timeZone': 'America/New_York',
        },
    }
    event = service.events().insert(calendarId='ENTER CALENDAR ID', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")

#add_calendar_event()
