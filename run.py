import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
from models.Kid import Kid
import re


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
ALL_KIDS = KIDS.get_all_records()
ALL_FOODS = FOODS.get_all_records()

# regular expressions
only_letters_regex = "^[a-zA-Z]+\s*"
age_regex = "^[1-3]$"
phone_number_regex = "\d{3}-\d{3}-\d{4}"
list_regex = "(^[a-z]+\s*[,]*)*"


def create_kid():
    """Create an user and add it to the database"""
    print('Creat a new kid')
    # get the variables from inputs
    name = validate_data("Name(only letters): \n", only_letters_regex)
    last_name = validate_data("Last name(only letters): \n", only_letters_regex)
    age = int(validate_data("Age(Number between 1 and 3): \n", age_regex))
    tutor = validate_data("Name of the tutor(only letters): \n", only_letters_regex)
    contact = validate_data("Contact number(must have this format: 123-456-7890): \n", phone_number_regex)
    allergies = validate_data("Allergies(only lowercase letters, if more than one, separated by commas. If no allergies, just leave it blank): \n", list_regex)
    # get last kid id from worksheet, if there is no kids yet, I have to assign 0, if not, it give me an error
    if len(ALL_KIDS) == 0:
        last_id = 0
    else:
        last_id = KIDS.row_values(len(ALL_KIDS) + 1)[0]
    # create an user and save it in the worksheet
    kid = Kid(name, last_name, age, tutor, contact, allergies)
    kid._get_id(int(last_id))
    KIDS.append_row(kid.kid_info())
    print(kid.kid_description())


def validate_data(inp, regex):
    """Check if data input have the correct format"""
    while True:
        data_to_check = input(inp)
        try:
            if re.search(regex, data_to_check):
                return data_to_check
            else:
                raise ValueError("Please enter the correct data format")
        except ValueError as error:
            print(error)


create_kid()
