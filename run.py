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

# create a boolean variable for each group and all the children. I have to know if the menu for all or each one of the groups have been created. I will created a dictionary with the necessary information about them
are_recipes_created = [
    {'group': 'all', 'created': False},
    {'group': 'green', 'created': False},
    {'group': 'blue', 'created': False},
    {'group': 'yellow', 'created': False}
]

# regular expressions
only_letters_regex = "[a-zA-Z\s']+"
age_regex = "[1-3]{1}"
phone_number_regex = "\d{3}-\d{3}-\d{4}"
list_regex = "(^[a-z,\s]+)*"


def create_data_choice():
    """
    Give the user the chance to create kid or recipe data and save it in the worksheet
    """
    print(txt.create_data)
    choice = None
    while choice == None:
        choice = input('Your choice:\n')
        if choice.upper() == 'K':
            create_kid()
        elif choice.upper() == 'R':
            create_recipe()
        else:
            choice = None


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
    ALL_KIDS = KIDS.get_all_records()
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
    print('Create a new recipe')
    # get the variables from the inputs
    name = help.validate_data('Name(only letters): \n', only_letters_regex)
    ingredients = help.validate_data('Ingredients(only lowercase letters, separated by commas: \n', list_regex)
    # get last food id from worksheet, if there is no food yet, I have to assign 0
    ALL_RECIPES = RECIPES.get_all_records()
    if len(ALL_RECIPES) == 0:
        last_id = 0
    else:
        last_id = RECIPES.row_values(len(ALL_RECIPES) + 1)[0]
    # create a food and save it in the worksheet
    recipe = Recipe(name, ingredients)
    recipe._get_id(int(last_id))
    RECIPES.append_row(recipe.recipe_info())
    print(recipe.recipe_description())


def retrive_data_choice():
    """
    Give the user the chance to rectrieve data from kids or recipes
    """
    print(txt.retrieve_data)
    choice = None
    while choice == None:
        choice = input('Your choice:\n')
        if choice.upper() == 'K':
            print(txt.retrieve_users)
            select = input('Your choice:\n')
            data = retrieve_kids_data(select)
            if len(data) == 1:
                help.print_kid_all_data(data[0])
            else:
                for kid in data:
                    help.print_kid(kid)
        elif choice.upper() == 'R':
            print(txt.retrieve_recipes)
            select = input('Your choice:\n')
            data = retrieve_recipe_data(select)
            if len(data) == 1:
                help.print_recipe_all_data(data[0])
            else:
                for recipe in data:
                    help.print_recipe(recipe)
        else:
            choice = None


def retrieve_kids_data(select):
    """
    Retrieve kids data from database. One particular kid, a group of kids by their color group or all the kids
    """
    ALL_KIDS = KIDS.get_all_records()
    if select.upper() == 'BLUE' or select.upper() == 'GREEN' or select.upper() == 'YELLOW':
        filter_list = [kid for kid in ALL_KIDS if kid['group'].upper() == select.upper()]
        return filter_list
    elif select.upper() == 'ALL':
        return ALL_KIDS
    else:
        kid = help.get_object_from_worksheet(select.upper(), ALL_KIDS)
        return kid


def retrieve_recipe_data(select):
    """
    Retrieve recipes data from database. One particular recipe or all of them
    """
    ALL_RECIPES = RECIPES.get_all_records()
    if select.upper() == 'ALL':
        return ALL_RECIPES
    else:
        recipe = help.get_object_from_worksheet(select.upper(), ALL_RECIPES)
        return recipe


def daily_menu():
    """
    Allows user to get a menu for children, if someone is alergic to any recipe, give user the possibility to get other recipe.
    """
    print(txt.daily_menu)
    check_created_recipes()
    # set to False the variables than are needed to run the app and give them a value inside a while loop
    kids = False
    while kids == False:
        group = input('Select the children:\n')
        kids = retrieve_kids_data(group)
    print(f"Children selected: {group.upper()}")
    # show the user all the recipes for their to choose one
    ALL_RECIPES = RECIPES.get_all_records()
    for recipe in ALL_RECIPES:
        help.print_recipe(recipe)
    recipe = False
    while recipe == False:
        id_input= input('Select a recipe by its id:\n')
        recipe = help.get_data_from_id(id_input, ALL_RECIPES)
    # find out if there are allergic kids to the recipe.
    is_someone_allergic = help.find_kids_allergic_to_recipe(kids, recipe['ingredients'].split(','))
    # if more than one list them and show what recipes they can eat, to the user choose one
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
        change_states_recipes(group)
    # if there is one, show him and the recipes that their can eat to the user to choose one
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
        change_states_recipes(group)
    else:
        print('There are no kids allergic to this recipe')
        print(f"Must be prepared {len(kids) - len(is_someone_allergic)} rations of {recipe['name']}")
        change_states_recipes(group)


def check_created_recipes():
    """
    Check if the daily menu have been created or not for any group or of all them.
    """
    for group in are_recipes_created:
        # If all the groups have a recipe assigned or the are an assigned recipe for all the children, the loop must be break, If not, the loop continue and shows if the are some group with or whitout an assigned recipe
        if group['group'] == 'all':
            if group['created'] == True:
                print('The daily menu for all the children is ALREADY assigned')
                break
        else:
            if group['created'] == True:
                print(f"The daily menu for the group {group['group'].upper()} is ALREADY assigned.")
            else:
                print(f"The daily menu for the group {group['group'].upper()} is NOT assigned yet.")
            


def change_states_recipes(group_assigned_menu):
    """"
    Change the state of a menu when it is created for the user
    """
    for group in are_recipes_created:
        if group['group'].upper() == group_assigned_menu.upper():
            group['created'] = True
    check_created_recipes()


def main():
    """
    Main function where the app is running
    """
    while True:
        print(txt.main_menu)
        inp = input('Your choice: \n')
        if inp.upper() == 'HELP':
            print(txt.help)
        elif inp.upper() == 'D':
            daily_menu()
        elif inp.upper() == 'R':
            retrive_data_choice()
        elif inp.upper() == 'C':
            create_data_choice()
        elif inp.upper() == 'EXIT':
            break


main()
# check_created_recipes()
