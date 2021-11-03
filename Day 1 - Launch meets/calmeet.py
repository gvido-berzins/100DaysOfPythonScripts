from __future__ import print_function
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import googleapiclient.discovery
import datetime
import os.path
import json
import webbrowser


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
google_resource = googleapiclient.discovery.Resource
SCRIPT_DIR = os.path.dirname(__file__)
CREDENTIALS_PATH = os.path.join(SCRIPT_DIR, 'credentials.json')
TOKEN_PATH = os.path.join(SCRIPT_DIR, 'token.json')


def authenticate() -> google_resource:
    """Authenticate and return the Resource object object"""
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(
            TOKEN_PATH, SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH,
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return googleapiclient.discovery.build('calendar', 'v3', credentials=creds)


def get_current_time():
    return datetime.datetime.utcnow().isoformat() + 'Z'


def get_events(service: google_resource, time_min: str, max_results: int = 10):
    result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return result.get('items', [])


def get_nth_latest_events(service: google_resource, time_min, max_results: int):
    return get_events(service, time_min, max_results)


def get_latest_event(service: google_resource, time_min):
    return get_events(service, time_min, max_results=1)[0]


def print_events(events):
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        link = event.get('hangoutLink')
        print(start, event['summary'], link)


def get_meeting_link(event):
    return event.get('hangoutLink')


def launch_latest_meeting(service, time_min) -> None:
    latest_event = get_latest_event(service, time_min)
    link = get_meeting_link(latest_event)
    webbrowser.open(link)


def jp(data):
    pretty_data = json.dumps(data, indent=2)
    print(pretty_data)
    return pretty_data


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar."""
    service = authenticate()
    time_now = get_current_time()
    launch_latest_meeting(service, time_now)
    exit()


if __name__ == '__main__':
    main()
