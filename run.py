import gspread
from google.oauth2.service_account import Credentials
import re
import json
from models.Kid import Kid
from models.Recipe import Recipe
from models.Daily_menu import Daily_menu
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
MENU = SH.worksheet('menu')

# regular expressions
only_letters_regex = "[a-zA-Z\s']+"
age_regex = "[1-3]{1}"
phone_number_regex = "\d{3}-\d{3}-\d{4}"
list_regex = "(^[a-z,\s]+)*"
only_numbers_regex = "[0-9]+"
group_of_kids_regex = re.compile("(green|blue|yellow|all)", re.I)
kid_or_recipe_regex = re.compile("(k|r)", re.I)


def create_data_choice():
    """
    Give the user the chance to create kid or recipe data and save it in the
    worksheet
    """
    help.print_splitter_dash()
    print(txt.create_data)
    help.print_splitter_dash()
    choice = help.validate_data('Your choice:\n', kid_or_recipe_regex)
    if choice.upper() == 'K':
        create_kid()
    elif choice.upper() == 'R':
        create_recipe()


def create_kid():
    """Create an user and add it to the database"""
    help.print_splitter_dash()
    print('Creat a new kid\n')
    # get the variables from inputs
    name = help.validate_data("Name(only letters): \n", only_letters_regex)
    last_name = help.validate_data("Last name(only letters): \n",
                                   only_letters_regex)
    age = int(help.validate_data("Age(Number between 1 and 3): \n",
                                 age_regex))
    tutor = help.validate_data("Name of the tutor(only letters): \n",
                               only_letters_regex)
    contact_input = "Contact number(must have this format: 123-456-7890): \n"
    contact = help.validate_data(contact_input, phone_number_regex)
    aller_iput = 'Allergies(lowercase, split by commas or leave it blank):\n'
    allergies = help.validate_data(aller_iput, list_regex)
    # get last kid id from worksheet, if there is no kids yet, I have to
    # assign 0, if not, it give me an error
    ALL_KIDS = KIDS.get_all_records()
    if len(ALL_KIDS) == 0:
        last_id = 0
    else:
        last_id = KIDS.row_values(len(ALL_KIDS) + 1)[0]
    # create an user and save it in the worksheet
    kid = Kid(name, last_name, age, tutor, contact, allergies)
    kid._get_id(int(last_id))
    KIDS.append_row(kid.kid_info())
    help.print_splitter_dash()
    print()
    print(kid.kid_description())
    print()
    help.print_continue_option()


def create_recipe():
    """
    Create a recipe and add it to the database
    """
    help.print_splitter_dash()
    print('Create a new recipe\n')
    # get the variables from the inputs
    name = help.validate_data('Name(only letters): \n', only_letters_regex)
    ing_input = 'Ingredients(only lowercase letters, separated by commas: \n'
    ingredients = help.validate_data(ing_input, list_regex)
    # get last food id from worksheet, if there is no food yet, I have to
    # assign 0
    ALL_RECIPES = RECIPES.get_all_records()
    if len(ALL_RECIPES) == 0:
        last_id = 0
    else:
        last_id = RECIPES.row_values(len(ALL_RECIPES) + 1)[0]
    # create a food and save it in the worksheet
    recipe = Recipe(name, ingredients)
    recipe._get_id(int(last_id))
    RECIPES.append_row(recipe.recipe_info())
    help.print_splitter_dash()
    print()
    print(recipe.recipe_description())
    print()
    help.print_continue_option()


def retrive_data_choice():
    """
    Give the user the chance to rectrieve data from kids or recipes
    """
    help.print_splitter_dash()
    print(txt.retrieve_data)
    help.print_splitter_dash()
    choice = help.validate_data('Your choice:\n', kid_or_recipe_regex)
    help.print_splitter_dash()
    if choice.upper() == 'K':
        print(txt.retrieve_users)
        help.print_splitter_dash()
        select = help.validate_data('Your choice(only letters):\n',
                                    only_letters_regex)
        data = retrieve_kids_data(select)
        help.print_splitter_dash()
        if len(data) == 1:
            help.print_kid_all_data(data[0])
            rem_p = ('Press R to remove kid or any letter to continue:\n')
            rem_inp = help.validate_data(rem_p, only_letters_regex)
            if rem_inp.upper() == 'R':
                confirm = help.validate_data('Are you sure? Y/N:\n',
                                             "(y|Y|n|N)")
                if confirm.upper() == 'Y':
                    help.remove_an_object(KIDS, str(data[0]['id']))
                elif confirm.upper() == 'N':
                    return
            else:
                return
        else:
            print()
            for kid in data:
                help.print_kid(kid)
            print()
        help.print_continue_option()
    elif choice.upper() == 'R':
        print(txt.retrieve_recipes)
        help.print_splitter_dash()
        select = help.validate_data('Your choice(only letters):\n',
                                    only_letters_regex)
        data = retrieve_recipe_data(select)
        help.print_splitter_dash()
        if len(data) == 1:
            help.print_recipe_all_data(data[0])
            rem_p = ('Press R to remove recipe or any letter to continue:\n')
            rem_inp = help.validate_data(rem_p, only_letters_regex)
            if rem_inp.upper() == 'R':
                confirm = help.validate_data('Are you sure? Y/N:\n',
                                             "(y|Y|n|N)")
                if confirm.upper() == 'Y':
                    help.remove_an_object(RECIPES, str(data[0]['id']))
                elif confirm.upper() == 'N':
                    return
            else:
                return
        else:
            print()
            for recipe in data:
                help.print_recipe(recipe)
            print()
        help.print_continue_option()


def retrieve_kids_data(select):
    """
    Retrieve kids data from database. One particular kid, a group of kids by
    their color group or all the kids
    """
    ALL_KIDS = KIDS.get_all_records()
    if (select.upper() == 'BLUE' or select.upper() == 'GREEN' or
       select.upper() == 'YELLOW'):
        filter_list = [
            kid for kid in ALL_KIDS if kid['group'].upper() == select.upper()
            ]
        return filter_list
    elif select.upper() == 'ALL':
        return ALL_KIDS
    else:
        kid = help.get_object_from_worksheet(select.upper(), ALL_KIDS)
        if kid:
            return kid
        else:
            return []


def retrieve_recipe_data(select):
    """
    Retrieve recipes data from database. One particular recipe or all of them
    """
    ALL_RECIPES = RECIPES.get_all_records()
    if select.upper() == 'ALL':
        return ALL_RECIPES
    else:
        recipe = help.get_object_from_worksheet(select.upper(), ALL_RECIPES)
        if recipe:
            return recipe
        else:
            return []


def daily_menu():
    """
    Allows user to get a menu for children, if someone is alergic to any recipe
    give user the possibility to get other recipe.
    """
    help.print_splitter_dash()
    print(txt.daily_menu)
    help.print_splitter_dash()
    are_menu_created = check_created_menus()
    # if None the user wants to come back to main menu, but if I send them to
    # main menu here, exit option does not work. That's why I return None
    if are_menu_created is None:
        return None
    print()
    help.print_splitter_dash()
    # get the date
    date = help.get_date()
    group = help.validate_data('Select the children:\n',
                               group_of_kids_regex)
    kids = retrieve_kids_data(group)
    help.print_splitter_dash()
    is_menu_created = help.is_menu_created(are_menu_created, group)
    if is_menu_created:
        print(f"The daily menu for the group {group} is already created\n")
        update = help.validate_data("Do you want to update it? Y/N\n",
                                    "(y|Y|n|N)")
        if update.upper() == 'N':
            return daily_menu()
        if update.upper() == 'Y':
            help.print_splitter_dash()
    print(f"Children selected: {group.upper()}\n")
    # show the user all the recipes for their to choose one
    ALL_RECIPES = RECIPES.get_all_records()
    for recipe in ALL_RECIPES:
        help.print_recipe(recipe)
    print()
    help.print_splitter_dash()
    id_input = int(help.validate_data('Select a recipe by its id:\n',
                                      only_numbers_regex))
    recipe = help.get_data_from_id(id_input, ALL_RECIPES)
    while not recipe:
        help.print_splitter_dash()
        print('Recipe not found. Enter valid Id\n')
        for recipe in ALL_RECIPES:
            help.print_recipe(recipe)
        print()
        help.print_splitter_dash()
        id_input = int(help.validate_data('Recipe Id:\n',
                                          only_numbers_regex))
        recipe = help.get_data_from_id(id_input, ALL_RECIPES)
    # find out if there are allergic kids to the recipe.
    is_someone_allergic = help.find_kids_allergic_to_recipe(
        kids, recipe['ingredients'].split(',')
        )
    # if more than one list them and show what recipes they can eat, to
    # the user choose one
    if len(is_someone_allergic) > 1:
        quantity = len(kids) - len(is_someone_allergic)
        allowed = []
        help.print_splitter_dash()
        lenght = len(is_someone_allergic)
        print()
        print(f'There are {lenght} kids allergic to this recipe')
        print('Choose another recipe for them\n')
        for kid in is_someone_allergic:
            help.print_splitter_dash()
            kid_allow_recipes = help.recipes_for_an_allergic_kid(kid,
                                                                 ALL_RECIPES)
            print(f"{kid['name']} {kid['last_name']} can eat:\n")
            for allow_recipe in kid_allow_recipes:
                help.print_recipe(allow_recipe)
            print()
            new_recipe_id = help.validate_data(
                'Choose the recipe by Id:\n', only_numbers_regex
                )
            new_recipe = help.get_data_from_id(new_recipe_id,
                                               kid_allow_recipes)
            while not new_recipe:
                help.print_splitter_dash()
                print('Recipe not found. Enter valid Id\n')
                for recipe in kid_allow_recipes:
                    help.print_recipe(recipe)
                print()
                help.print_splitter_dash()
                id_input = int(help.validate_data('Recipe Id:\n',
                                                  only_numbers_regex))
                new_recipe = help.get_data_from_id(id_input, kid_allow_recipes)
            if new_recipe in allowed:
                new_recipe['quantity'] += 1
                new_recipe['kids_id'].append(kid['id'])
            else:
                new_recipe['quantity'] = 1
                allowed.append(new_recipe)
                new_recipe['kids_id'] = [kid['id']]
            print(f"""
Recipe {new_recipe['name']} selected for {kid['name']} {kid['last_name']}\n""")
        help.print_splitter_dash()
        print(f"""
Must be prepared {len(kids) - lenght} rations of {recipe['name']}""")
        for new_recipe in allowed:
            if new_recipe['quantity'] > 1:
                print(f"""
Must be prepared {new_recipe['quantity']} rations of {new_recipe['name']}""")
            else:
                print(f"""
Must be prepared {new_recipe['quantity']} ration of {new_recipe['name']}""")
        print()
        # create an instance an add the data to the worksheet
        menu_data = Daily_menu(date,
                               group,
                               recipe,
                               quantity,
                               allowed)._get_properties()
        if is_menu_created:
            help.update_menu(MENU, date, menu_data[2], group)
        else:
            MENU.append_row(menu_data)
        help.print_continue_option()
    # if there is one, show the recipes that they can eat to the
    # user to choose one
    elif len(is_someone_allergic) == 1:
        kid = is_someone_allergic[0]
        quantity = len(kids) - 1
        help.print_splitter_dash()
        print()
        print('There is 1 kid allergic to this recipe')
        print('Choose another recipe for they\n')
        kid_allow_recipes = help.recipes_for_an_allergic_kid(kid, ALL_RECIPES)
        help.print_splitter_dash()
        print(f"{kid['name']} {kid['last_name']} can eat:\n")
        for allow_recipe in kid_allow_recipes:
                help.print_recipe(allow_recipe)
        print()
        new_recipe_id = help.validate_data('Choose the recipe by Id: \n',
                                           only_numbers_regex)
        new_recipe = help.get_data_from_id(new_recipe_id,
                                           kid_allow_recipes)
        while not new_recipe:
            help.print_splitter_dash()
            print('Recipe not found. Enter valid Id\n')
            for recipe in kid_allow_recipes:
                help.print_recipe(recipe)
            print()
            help.print_splitter_dash()
            id_input = int(help.validate_data('Recipe Id:\n',
                                              only_numbers_regex))
            new_recipe = help.get_data_from_id(id_input, kid_allow_recipes)
        print(f"""
Recipe {new_recipe['name']} selected for {kid['name']} {kid['last_name']}\n""")
        help.print_splitter_dash()
        print()
        print(f"Must be prepared {quantity} rations of {recipe['name']}\n")
        print(f"Must be prepared 1 ration of {new_recipe['name']}\n")
        # add the kid id and quantity properties to the recipe
        new_recipe['kids_id'] = [kid['id']]
        new_recipe['quantity'] = 1
        # create an instance an add the data to the worksheet
        menu_data = Daily_menu(date,
                               group,
                               recipe,
                               quantity,
                               [new_recipe])._get_properties()
        if is_menu_created:
            help.update_menu(MENU, date, menu_data[2], group)
        else:
            MENU.append_row(menu_data)
        help.print_continue_option()
    else:
        help.print_splitter_dash()
        quantity = len(kids)
        print()
        print('There are no kids allergic to this recipe\n')
        print(f"Must be prepared {quantity} rations of {recipe['name']}\n")
        # create an instance an add the data to the worksheet
        menu_data = Daily_menu(date, group, recipe, quantity)._get_properties()
        if is_menu_created:
            help.update_menu(MENU, date, menu_data[2], group)
        else:
            MENU.append_row(menu_data)
        help.print_continue_option()
    return main()


def check_created_menus():
    """
    Check if the daily menu have been created or not for any group or of
    all them.
    """
    ALL_MENUS = MENU.get_all_records()
    ALL_RECIPES = RECIPES.get_all_records()
    ALL_KIDS = KIDS.get_all_records()
    date = help.get_date()
    # check if a menu for the day is already created
    are_menu_created = []
    for menu in ALL_MENUS:
        if menu['date'] == date:
            are_menu_created.append({
                'group': menu['group'],
                'daily_menu': json.loads(menu['menu'])
            })
    # if there is no a menu
    if len(are_menu_created) == 0:
        print()
        print('There is no daily menu created yet')
        while True:
            create_or_main_inp = """
Press C to create a new menu or any key to go to main menu\n"""
            create_or_main = help.validate_data(create_or_main_inp,
                                                "\w")
            if create_or_main.upper() == 'C':
                return are_menu_created
            else:
                return main()
    # if one or more menu already exists
    else:
        created_groups = [group['group'].upper() for group in are_menu_created]
        if 'ALL' in created_groups:
            print()
            print('The daily menu for ALL the children is ALREADY created')
            while True:
                show_menu_inp = """
Press S to see the menu, C to create a new menu, M to go back to main menu\n"""
                show_menu = help.validate_data(show_menu_inp,
                                               only_letters_regex)
                if show_menu.upper() == 'S':
                    menu = [
                        all for all in are_menu_created
                        if all['group'].upper() == 'ALL'
                        ]
                    help.print_menu(menu, ALL_RECIPES, ALL_KIDS)
                    rem_p = ('Press R to remove menu, any key to continue:\n')
                    rem_inp = help.validate_data(rem_p, only_letters_regex)
                    if rem_inp.upper() == 'R':
                        confirm = help.validate_data('Are you sure? Y/N:\n',
                                                     "(y|Y|n|N)")
                        if confirm.upper() == 'Y':
                            help.remove_an_object(MENU, None, date)
                            return main()
                        elif confirm.upper() == 'N':
                            return main()
                    else:
                        return main()
                elif show_menu.upper() == 'C':
                    return are_menu_created
                elif show_menu.upper() == 'M':
                    return main()
        else:
            for group in are_menu_created:
                print(f"""
The daily menu for the group {group['group'].upper()} is ALREADY created.""")
            while True:
                show_menu_inp = """
Press S to see the menu, C to create a new menu, M to go back to main menu\n"""
                show_menu = help.validate_data(show_menu_inp,
                                               only_letters_regex)
                if show_menu.upper() == 'S':
                    menus = [
                        group for group in are_menu_created
                        if group['group'].upper() != 'ALL'
                        ]
                    help.print_menu(menus, ALL_RECIPES, ALL_KIDS)
                elif show_menu.upper() == 'C':
                    return are_menu_created
                elif show_menu.upper() == 'M':
                    return main()


def main():
    """
    Main function where the app is running
    """
    while True:
        help.print_splitter_dash()
        print(txt.main_menu)
        help.print_splitter_dash()
        inp = help.validate_data('Your choice:\n', only_letters_regex)
        if inp.upper() == 'HELP':
            help.print_splitter_dash()
            print(txt.help)
            help.print_continue_option()
        elif inp.upper() == 'D':
            return daily_menu()
        elif inp.upper() == 'R':
            retrive_data_choice()
        elif inp.upper() == 'C':
            create_data_choice()
        elif inp.upper() == 'EXIT':
            break

print(txt.welcome)
main()
