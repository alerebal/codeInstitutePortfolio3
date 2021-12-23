import re


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


