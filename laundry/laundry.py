from sheet_setup import get_sheets_service


SHEET_ID = '1RWbJbJKzbKyeqoI4pzYqBPM1rypFNHFgganUnwqc534'
RANGE = 'J1:K2'
service = get_sheets_service()
sheet = service.spreadsheets()
result_input = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE).execute()
values_input = result_input.get('values', [])
