import re


def validate_data(inp, regex):
    """
    Check if data input have the correct format
    """
    while True:
        data_to_check = input(inp)
        try:
            if re.fullmatch(regex, data_to_check):
                return data_to_check
            else:
                raise ValueError("Please enter the correct data format")
        except ValueError as error:
            print(error)


def get_object_from_worksheet(name, worksheet):
    """
    Get an object by their name in case that just one user exists with that name in the worksheet. Otherwise, the object id will be used. 
    """   
    obj_list = []
    for obj in worksheet:
        if obj['name'].upper().find(name.upper()) != -1:
            obj_list.append(obj)
    if len(obj_list) < 1:
        print('Data could not been found')
        return False
    elif len(obj_list) == 1:
        return obj_list[0]
    else:
        print('There are more than 1 coincidence with that name')
        return obj_list
        

def get_data_from_id(id, data_list):
    """
    Get an id and looking for an object in a list of dictionaries
    """
    for data in data_list:
        if data['id'] == int(id):
            return data
    return False


def print_kid(kid):
    """
    Print a kid data with their id, name and last name
    """
    print(f"Id: {kid['id']} - {kid['name']} {kid['last_name']}")


def print_recipe(recipe):
    """
    Print a recipe with its id and its name
    """
    print(f"Id: {recipe['id']} - {recipe['name']}.")


def find_kids_allergic_to_recipe(kids, ingredients):
    """
    Find any kid or kids with allergies to some or several ingredients  
    """
    kids_allergic_to_recipe = []
    for kid in kids:
        if not kid['allergies'] == '':
            # I have to take off the blank spaces in both ingredients and allergies for them to match
            kid_allergies = [aller.strip() for aller in kid['allergies'].split(',')]
            for ing in ingredients:
                if ing.strip() in kid_allergies:
                    kids_allergic_to_recipe.append(kid)
    return kids_allergic_to_recipe


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
