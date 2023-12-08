import gspread
from google.oauth2.service_account import Credentials
# Define the scope
scope = ['https://www.googleapis.com/auth/spreadsheets']
# Add credentials to the account
creds = Credentials.from_service_account_file('service_account.json', scopes=scope)
# Authorize the clientsheet
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open('Class Coordinator').sheet1  # Or use .worksheet('Sheet1')

# Data to be inserted
row = ["Value1", "Value2", "Value3"]  # Update with the data you want to insert

# Insert the row
sheet.append_row(row)
