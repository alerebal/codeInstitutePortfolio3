class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def _get_id(self, last_id):
        self.recipe_id = last_id + 1

    def recipe_info(self):
        return [self.recipe_id, self.name, self.ingredients]

    def recipe_description(self):
        return f"Recipe {self.name} has been created with id: {self.recipe_id} "
    