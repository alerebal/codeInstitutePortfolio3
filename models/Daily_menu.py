import json


class Daily_menu:
    def __init__(self, date, group, main_recipe, qty, allergics=[]):
        self.date = date
        self.group = group
        self.main_recipe = main_recipe
        self.qty = qty
        self.allergics = allergics

    def _get_properties(self):
        """
        Create the daily menu dictionary according to the recipes received and
        return the data needed to add a row to the worksheet.
        """
        self.daily_menu = {
            'main_recipe': {
                'recipe_id': self.main_recipe['id'],
                'quantity': self.qty
            }}
        if len(self.allergics) > 0:
            self.daily_menu['allergic_recipes'] = []
            for allergic in self.allergics:
                self.daily_menu['allergic_recipes'].append(allergic)
        # Convert the dictionary to string and return the data to the worksheet
        return [self.date, self.group, json.dumps(self.daily_menu)]
