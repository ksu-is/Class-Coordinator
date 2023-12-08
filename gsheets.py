import gspread
from google.oauth2.service_account import Credentials
# Define the scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
# Add credentials to the account
def add_assignment(assignment_title,assignment_date):
    creds = Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
    # Authorize the clientsheet
    client = gspread.authorize(creds)

    #sheet = client.create('Class Coordinator')

    # Open the sheet
    sheet = client.open('Class Coordinator').sheet1  # Or use .worksheet('Sheet1')

    # Data to be inserted
    row = [assignment_title,assignment_date]  # Update with the data you want to insert

    # Insert the row
    sheet.append_row(row)
