import json

class Daily_menu:
    def __init__(self, date, group, main_recipe, qty, allergics = []):
        self.date = date
        self.group = group
        self.main_recipe = main_recipe
        self.qty = qty
        self.allergics = allergics


    def _get_properties(self):
        self.daily_menu = {
            'main_recipe' :{
            'recipe_id': self.main_recipe['id'],
            'quantity': self.qty
        }}
        if len(self.allergics) > 0:
            self.daily_menu['allergic_recipes'] = []
            for allergic in self.allergics:
                self.daily_menu['allergic_recipes'].append(allergic)
        # return the data to add to the worksheet. Convert the object to string
        return [self.date, self.group, json.dumps(self.daily_menu)]

        
