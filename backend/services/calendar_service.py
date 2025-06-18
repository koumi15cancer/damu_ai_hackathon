from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
from datetime import datetime, timedelta
from config import SCOPES, CALENDAR_SETTINGS

class CalendarService:
    def __init__(self):
        self.creds = None
        self.service = None

    def authenticate(self):
        """Authenticate with Google Calendar API."""
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_free_time_slots(self, calendar_ids, start_date=None, end_date=None):
        """Get free time slots for a list of calendar IDs."""
        if not start_date:
            start_date = datetime.utcnow()
        if not end_date:
            end_date = start_date + timedelta(days=CALENDAR_SETTINGS['look_ahead_days'])

        # Get busy periods for all calendars
        busy_periods = []
        for calendar_id in calendar_ids:
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=start_date.isoformat() + 'Z',
                timeMax=end_date.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                busy_periods.append({
                    'start': datetime.fromisoformat(start.replace('Z', '+00:00')),
                    'end': datetime.fromisoformat(end.replace('Z', '+00:00'))
                })

        # Find common free time slots
        free_slots = self._find_common_free_slots(busy_periods, start_date, end_date)
        return free_slots

    def _find_common_free_slots(self, busy_periods, start_date, end_date):
        """Find common free time slots between all calendars."""
        # Sort busy periods by start time
        busy_periods.sort(key=lambda x: x['start'])
        
        free_slots = []
        current_time = start_date
        
        for period in busy_periods:
            if current_time < period['start']:
                free_slots.append({
                    'start': current_time,
                    'end': period['start']
                })
            current_time = max(current_time, period['end'])
        
        if current_time < end_date:
            free_slots.append({
                'start': current_time,
                'end': end_date
            })
        
        # Filter out slots shorter than 2 hours
        return [slot for slot in free_slots 
                if (slot['end'] - slot['start']).total_seconds() >= 7200] 