import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = '1RWbJbJKzbKyeqoI4pzYqBPM1rypFNHFgganUnwqc534'
RANGE = 'Stuff!K1:L2'

def get_sheets_service():
    laundry_list = []
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE).execute()
    values_input = result_input.get('values', [])
    money_on_card = values_input[1][0]
    loads_left = values_input[1][1]
    laundry_list.append(money_on_card)
    laundry_list.append(loads_left)
    return laundry_list

if __name__ == "__main__":
    get_sheets_service()