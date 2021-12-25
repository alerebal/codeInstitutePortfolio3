import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
from models.Kid import Kid
from models.Recipe import Recipe
import helpers.helpers as help
from helpers import help_texts as txt

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
    name = help.validate_data("Name(only letters): \n", only_letters_regex)
    last_name = help.validate_data("Last name(only letters): \n", only_letters_regex)
    age = int(help.validate_data("Age(Number between 1 and 3): \n", age_regex))
    tutor = help.validate_data("Name of the tutor(only letters): \n", only_letters_regex)
    contact = help.validate_data("Contact number(must have this format: 123-456-7890): \n", phone_number_regex)
    allergies = help.validate_data("Allergies(only lowercase letters, if more than one, separated by commas. If no allergies, just leave it blank): \n", list_regex)
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
    name = help.validate_data('Name(only letters): \n', only_letters_regex)
    ingredients = help.validate_data('Ingredients(only lowercase letters, separated by commas: \n', list_regex)
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


def daily_menu():
    """
    Allows user to get a menu for children, if someone is alergic to any recipe, give user the possibility to get other recipe.
    """
    print(txt.daily_menu)
    kids = None
    while kids == None:
        select = input('Select the children:\n')
        kids = retrieve_kids_data(select)
    for recipe in ALL_RECIPES:
        help.print_recipe(recipe)
    recipe = False
    while recipe == False:
        id_input= input('Select a recipe by its id:\n')
        recipe = help.get_data_from_id(id_input, ALL_RECIPES)
    is_someone_allergic = help.find_kids_allergic_to_recipe(kids, recipe['ingredients'].split(','))
    if len(is_someone_allergic) > 1:
        allowed = []
        print(f'There are {len(is_someone_allergic)} kids allergic to this recipe')
        print('Choose another recipe for them\n')
        for kid in is_someone_allergic:
            kid_allow_recipes = help.recipes_for_an_allergic_kid(kid, ALL_RECIPES)
            print(f"{kid['name']} {kid['last_name']} can eat:")
            for allow_recipe in kid_allow_recipes:
                help.print_recipe(allow_recipe)
            print('')
            new_recipe = False
            while new_recipe == False:
                new_recipe_id = input('Choose the recipe by Id: \n')
                new_recipe = help.get_data_from_id(new_recipe_id, kid_allow_recipes)
            if new_recipe in allowed:
                new_recipe['quantity'] += 1
            else:
                new_recipe['quantity'] = 1
                allowed.append(new_recipe)
        print(f"Must be prepared {len(kids) - len(is_someone_allergic)} rations of {recipe['name']}")
        for new_recipe in allowed:
            if new_recipe['quantity'] > 1:
                print(f"Must be prepared {new_recipe['quantity']} rations of {new_recipe['name']}")
            else:
                print(f"Must be prepared {new_recipe['quantity']} ration of {new_recipe['name']}")
    elif len(is_someone_allergic) == 1:
        kid = is_someone_allergic[0]
        print('There is a kid allergic to this recipe')
        print('Choose another recipe for they\n')
        kid_allow_recipes = help.recipes_for_an_allergic_kid(kid, ALL_RECIPES)
        print(f"{kid['name']} {kid['last_name']} can eat:")
        for allow_recipe in kid_allow_recipes:
                help.print_recipe(allow_recipe)
        new_recipe = False
        while new_recipe == False:
            new_recipe_id = input('Choose the recipe by Id: \n')
            new_recipe = help.get_data_from_id(new_recipe_id, kid_allow_recipes)
        print(f"Must be prepared {len(kids) - len(is_someone_allergic)} rations of {recipe['name']}")
        print(f"Must be prepared 1 ration of {new_recipe['name']}")
    else:
        print('There are no kids allergic to this recipe')
        print(f"Must be prepared {len(kids) - len(is_someone_allergic)} rations of {recipe['name']}")


def retrive_data_choice():
    """
    Give the user the chance to rectrieve data from kids or recipes
    """
    print(txt.retrieve_data)
    choice = input('Your choice:\n')
    if choice.upper() == 'K':
        print(txt.retrieve_users)
        select = input('Your chioce:\n')
        retrieve_kids_data(select)
    elif choice.upper() == 'R':
        print(txt.retrieve_recipes)
        select = input('Your choice:\n')
        retrieve_recipe_data(select)


def retrieve_kids_data(select):
    """
    Retrieve kids data from database. One particular kid, a group of kids by their color group or all the kids
    """
    if select.upper() == 'BLUE' or select.upper() == 'GREEN' or select.upper() == 'YELLOW':
        filter_list = [kid for kid in ALL_KIDS if kid['group'].upper() == select.upper()]
        # pprint(filter_list, sort_dicts=False)
        return filter_list
    elif select.upper() == 'ALL':
        # pprint(ALL_KIDS)
        return ALL_KIDS
    else:
        get_object_from_worksheet(select.upper(), 'kids')


def retrieve_recipe_data(select):
    """
    Retrieve recipes data from database. One particular recipe or all of them
    """
    if select.upper() == 'ALL':
        # pprint(ALL_RECIPES)
        return ALL_RECIPES
    else:
        recipe = get_object_from_worksheet(select.upper(), 'recipes')
        return recipe


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
        selected_obj = help.get_data_from_id(id, ws)
        if worksheet == 'kids':
            print(f"{selected_obj['name']} {selected_obj['last_name']} selected")
        elif worksheet == 'recipes':
            print(f"{selected_obj['name']} with id {selected_obj['id']} selected")
        pprint(selected_obj)
        return selected_obj


def main():

    print(txt.welcome)
    while True:
        inp = input('Your choice: \n')
        if inp.upper() == 'HELP':
            print(help.help)
        elif inp.upper() == 'D':
            return daily_menu()
        elif inp.upper() == 'R':
            return retrive_data_choice()
        elif inp.upper() == 'C':
            return print('Create data')


main()
