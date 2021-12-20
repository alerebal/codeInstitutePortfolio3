import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

SH = GSPREAD_CLIENT.open('daily_menu_management')
KIDS = SH.worksheet('kids')
FOODS = SH.worksheet('foods')

pprint(KIDS.get_all_values())
pprint(FOODS.get_all_values())
