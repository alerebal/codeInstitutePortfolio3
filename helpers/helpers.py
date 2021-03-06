import re
import datetime


def validate_data(inp, regex):
    """
    Check if data input have the correct format
    """
    while True:
        data_to_check = input(inp).strip()
        try:
            if re.fullmatch(regex, data_to_check):
                return data_to_check
            else:
                raise ValueError("Please enter the correct data format")
        except ValueError as error:
            print(error)


def get_object_from_worksheet(name, worksheet):
    """
    Get an object by their name in case that just one user exists with that
    name in the worksheet. Otherwise, the object id will be used. The object
    must be send into a list.
    """
    obj_list = []
    for obj in worksheet:
        if obj['name'].upper().find(name.upper()) != -1:
            obj_list.append(obj)
    if len(obj_list) < 1:
        print('Data could not be found')
        return False
    elif len(obj_list) == 1:
        return obj_list
    else:
        print_splitter_dash()
        print("""There are more than 1 coincidence with that description.
Choose one by Id\n""")
        for obj in obj_list:
            # If the object is a kid, can be more than one kid with the same
            # name,so if the object has last name property show more
            # information on screen
            if obj.get('last_name'):
                print(f"Id: {obj['id']} - {obj['name']} {obj['last_name']}")
            else:
                print(f"Id: {obj['id']} - {obj['name']}")
        print()
        print_splitter_dash()
        # selected_obj = False
        # while selected_obj == False:
        obj_id = int(validate_data('Your choice:\n', '[0-9]+'))
        selected_obj = get_data_from_id(obj_id, obj_list)
        while not selected_obj:
            print_splitter_dash()
            print('Enter valid Id\n')
            obj_id = int(validate_data('Your choice:\n', '[0-9]+'))
            selected_obj = get_data_from_id(obj_id, obj_list)
        return [selected_obj]


def get_data_from_id(id, data_list):
    """
    Get an id and looking for an object in a list of dictionaries
    """
    for data in data_list:
        if data['id'] == int(id):
            return data
    return False


def print_splitter_dash():
    """
    Print a dashed splitter of 80 columns
    """
    print('-' * 80)


def print_kid(kid):
    """
    Print a kid data with their id, name and last name
    """
    print(f"Id: {kid['id']} - {kid['name']} {kid['last_name']}")


def print_kid_all_data(kid):
    """
    Print all the data of a kid, without kid_id
    """
    if kid['allergies'] != '':
        # The indentation is rere, otherwise, it put space or tabs in the
        # print statement
        print(f"""
Name: {kid['name']}
Last name: {kid['last_name']}
Age: {kid['age']}
Tutor: {kid['tutor']}
Contact: {kid['contact_number']}
Group: {kid['group']}
Allergies: {kid['allergies']}
""")
    else:
        print(f"""
Name: {kid['name']}
Last name: {kid['last_name']}
Age: {kid['age']}
Tutor: {kid['tutor']}
Contact: {kid['contact_number']}
Group: {kid['group']}
Allergies: no allergies
""")


def print_recipe(recipe):
    """
    Print a recipe with its id and its name
    """
    print(f"Id: {recipe['id']} - {recipe['name']}.")


def print_recipe_all_data(recipe):
    """
    Print all the data of a recipe, without recipe_id
    """
    print(f"""
Recipe: {recipe['name']}
Ingredients: {recipe['ingredients']}
""")


def print_continue_option():
    """
    Print a continue option to add to the bottom of the data show to the user
    """
    return input('Press enter to continue\n')


def find_kids_allergic_to_recipe(kids, ingredients):
    """
    Find any kid or kids with allergies to some or several ingredients
    """
    kids_allergic = []
    for kid in kids:
        if not kid['allergies'] == '':
            # I have to take off the blank spaces in both ingredients and
            # allergies for them to match
            kid_allergies = [
                aller.strip() for aller in kid['allergies'].split(',')
                ]
            for ing in ingredients:
                if ing.strip() in kid_allergies and kid not in kids_allergic:
                    kids_allergic.append(kid)
    return kids_allergic


def recipes_for_an_allergic_kid(kid, recipes):
    """
    Find all the recipes that an allergic kid can eat from a list of recipes
    """
    allergies = [aller.strip() for aller in kid['allergies'].split(',')]
    allow_recipes = []
    for recipe in recipes:
        ingredients = [ing.strip() for ing in recipe['ingredients'].split(',')]
        for aller in allergies:
            if aller in ingredients:
                recipe['not allowed'] = True
        if not recipe.get('not allowed'):
            allow_recipes.append(recipe)
    return allow_recipes


def print_menu(menus, list_of_recipes, list_of_kids):
    for menu in menus:
        main_recipe = get_data_from_id(
            menu['daily_menu']['main_recipe']['recipe_id'],
            list_of_recipes
            )
        quantity = menu['daily_menu']['main_recipe']['quantity']
        group = menu['group'].upper()
        print_splitter_dash()
        print()
        print(f"Group: {group}\n")
        print(f"""Main recipe: {main_recipe['name']}
Rations: {quantity}\n""")
        if 'allergic_recipes' in menu['daily_menu'].keys():
            allergic_recipes = menu['daily_menu']['allergic_recipes']
            for recipe in allergic_recipes:
                allergic_recipe = get_data_from_id(recipe['id'],
                                                   list_of_recipes)
                quantity = recipe['quantity']
                kids_id = recipe['kids_id']
                print(f"""Allergic recipe: {allergic_recipe['name']}
Rations: {quantity}
For:""")
                for id in kids_id:
                    kid = get_data_from_id(id, list_of_kids)
                    print(f"{kid['name']} {kid['last_name']}")
                print()


def get_date():
    """
    Get the date and give it a format month-day-number of day (Dec-Mon-23)
    """
    date_raw = datetime.datetime.now()
    return date_raw.strftime('%b-%a-%d')


def update_menu(worksheet, date, data_to_update, group):
    """
    Update a menu in the worksheet. Date is the string to looking for(we are
    looking for a specific date), data to update is what we want to modificate
    and group is essential because we can have more than menu for a specific
    date
    """
    menus = worksheet.findall(date)
    for menu in menus:
        row_number = menu.row
        if group.upper() in worksheet.row_values(row_number)[1].upper():
            worksheet.update_cell(row_number, 3, data_to_update)


def is_menu_created(created_menus, group):
    """
    Returns True if the menu for a group of kids already exists.
    """
    for menu in created_menus:
        if menu['group'].upper() == group.upper():
            return True


def remove_an_object(worksheet, obj_id=None, date=None):
    """
    Remove an object from the worksheet. If I want to remove a recipe or a kid
    I will need the obj_id number and if I want to remove a menu for all the
    kids I will need the date parameter.
    """
    if obj_id:
        obj_to_remove = worksheet.find(obj_id)
        if obj_to_remove:
            row_number = obj_to_remove.row
            worksheet.delete_rows(row_number)
            print_splitter_dash()
            print()
            print('Removed successfully\n')
    if date:
        menus = worksheet.findall(date)
        for menu in menus:
            row_number = menu.row
            if 'ALL' in worksheet.row_values(row_number)[1].upper():
                worksheet.delete_rows(row_number)
                print_splitter_dash()
                print()
                print('Removed successfully\n')
