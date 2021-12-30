class Daily_menu:
    def __init__(self, date, main_recipe, qty, allergics = []):
        self.date = date
        self.main_recipe = main_recipe
        self.qty = qty
        self.allergics = allergics


    def _get_properties(self):
        self.daily_menu = {
            'recipe_id': self.main_recipe['id'],
            'quantity': self.qty
        }
        if len(self.allergics) == 1:
            self.daily_menu['allergic_recipes'] = []
            self.daily_menu['allergic_recipes'].append({
                    'recipe_id': self.allergics[0]['id'],
                    'quantity': 1
                })
        if len(self.allergics) > 1:
            self.daily_menu['allergic_recipes'] = []
            for recipe in self.allergics:
                self.daily_menu['allergic_recipes'].append({
                    'recipe_id': recipe['id'],
                    'quantity': recipe['quantity']
                })
        return self.daily_menu
        
