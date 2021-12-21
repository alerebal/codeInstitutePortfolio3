class Food:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def _get_id(self, last_id):
        self.food_id = last_id + 1

    def food_info(self):
        return [self.food_id, self.name, self.ingredients]

    def food_description(self):
        return f"Food {self.name} has been created with id: {self.food_id} "
    