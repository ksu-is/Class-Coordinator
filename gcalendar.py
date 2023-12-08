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

def add_calendar_event():
    service = get_calendar_service()

    # Call the Calendar API
    event = {
        'summary': 'Appointment',
        'location': 'Somewhere',
        'description': 'A chance to talk.',
        'start': {
            'dateTime': '2023-12-10T10:00:00-07:00',
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': '2023-12-10T11:00:00-07:00',
            'timeZone': 'America/New_York',
        },
    }
    event = service.events().insert(calendarId='f53a5b77c3635eebd4b7d2ae212eb6fd54f5ef53c0ecf73aaa8b8e37eda3b46d@group.calendar.google.com', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")

#add_calendar_event()
