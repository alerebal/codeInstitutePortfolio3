class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def _get_id(self, last_id):
        """
        Set the recipe_id property adding 1 to the last recipe_id in worksheet
        """
        self.recipe_id = last_id + 1

    def recipe_info(self):
        """
        Return the necessary data to create a row in the worksheet
        """
        return [self.recipe_id, self.name, self.ingredients]

    def recipe_description(self):
        """
        Return the success message to show to the user
        """
        return f"The data of {self.name} has been created"
