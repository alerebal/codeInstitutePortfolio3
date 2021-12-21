import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
from models.Kid import Kid
from models.Recipe import Recipe
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
RECIPES = SH.worksheet('recipes')
ALL_KIDS = KIDS.get_all_records()
ALL_RECIPES = RECIPES.get_all_records()

# regular expressions
only_letters_regex = "[a-zA-Z\s']+"
age_regex = "[1-3]{1}"
phone_number_regex = "\d{3}-\d{3}-\d{4}"
list_regex = "(^[a-z,\s]+)*"


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


def create_recipe():
    """
    Create a recipe and add it to the database
    """
    print('Create a new food')
    # get the variables from the inputs
    name = validate_data('Name(only letters): \n', only_letters_regex)
    ingredients = validate_data('Ingredients(only lowercase letters, separated by commas: \n', list_regex)
    # get last food id from worksheet, if there is no food yet, I have to assign 0
    if len(ALL_RECIPES) == 0:
        last_id = 0
    else:
        last_id = RECIPES.row_values(len(ALL_RECIPES) + 1)[0]
    # create a food and save it in the worksheet
    recipe = Recipe(name, ingredients)
    recipe._get_id(int(last_id))
    RECIPES.append_row(recipe.recipe_info())
    print(recipe.recipe_description())


def get_object_from_worksheet(name, worksheet):
    """
    Get an object by their name in case that just one user exists with that name in the worksheet. Otherwise, the object id will be used. 
    """   
    ws = SH.worksheet(worksheet).get_all_records()
    objt_list = []
    for obj in ws:
        if obj['name'].upper().find(name.upper()) != -1:
            objt_list.append(obj)
    if len(objt_list) < 1:
        print('Data could not been found')
        return False
    elif len(objt_list) == 1:
        print(objt_list[0])
        return objt_list[0]
    else:
        print('There are more than 1 coincidence with that name')
        for obj in objt_list:
            if worksheet == 'kids':
                print(f"{obj['name']} {obj['last_name']}- Id: {obj['id']}")
            elif worksheet == 'recipes':
                print(f"{obj['name']} with ingredients: {obj['ingredients']} - Id: {obj['id']}")
        id = int(input("Choise one by Id:\n"))
        selected_obj = get_data_from_id(id, ws)
        if worksheet == 'kids':
            print(f"{selected_obj['name']} {selected_obj['last_name']} selected")
        elif worksheet == 'recipes':
            print(f"{selected_obj['name']} with id {selected_obj['id']} selected")
        pprint(selected_obj)
        return selected_obj

def get_data_from_id(id, data_list):
    """
    Get an id and looking for an object in a list of dictionaries
    """
    for data in data_list:
        if data['id'] == int(id):
            return data
    return False


def validate_data(inp, regex):
    """Check if data input have the correct format"""
    while True:
        data_to_check = input(inp)
        try:
            if re.fullmatch(regex, data_to_check):
                return data_to_check
            else:
                raise ValueError("Please enter the correct data format")
        except ValueError as error:
            print(error)


create_recipe()
