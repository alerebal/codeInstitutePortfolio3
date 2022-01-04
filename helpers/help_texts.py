welcome = """Welcome to Daily Menu APP

Create a daily menu for your primary school.
Keep a record, create, retrieve or upload the data. 
The data you can recording are:
Daily menu: a main recipe for all the children or a group of them.
In case someone were allergic to the main recipe, one recipe for they.
Kids: Their name, age and group who they belong, tutor details and any allergy 
if they have one.
Recipes: name and ingredients.
"""

main_menu = """Main menu

Press D to daily menu.
Press R to retrieve data.
Press C to create data.
Press Help to get help or information about the app.
Press Exit to exit
"""

help = """Help

Daily menu: 
Choose all the children or a group of them.
Choose a receipe from the list of recipes and check if any of them are allergic
to any ingredient in the recipe.
If no one is allergic, the recipe will be assigned to the menu, otherwise, 
choose any recipe for allergic children from a specific list that includes all
the recipes allowed for those children.
The menu for all children always prevails over the groups.

Retrieve data:
Get data about one specific child by their name or id, sorted by their group or
all of the children.
Get data on any recipe by name or ID, or get all recipes.

Create data:
Create data of a child following different steps. The system will guide you 
asking for different information about the child that is needed to create one.
Create data of a recipe in the same way as to create a kid.
"""

daily_menu = """Daily menu:

Choose a group of kids(enter BLUE, YELLOW or GREEN) or all of them(enter ALL).
After that, choose a recipe by its ID from the list shown.
If one or more kids are allergic to the recipe, a list of allowed recipes for 
each kid will be shown and you will be able to choice another recipe for those 
kids.
"""

create_data = """Create data:

Press K to create data of a kid.
Press R to create data of a recipe.
"""

retrieve_data = """Retrieve data:

Press K to retrieve kids data.
Press R to retrieve recipes data. 
"""

retrieve_users = """Retrieve kids data:

If you want to get data of one particular kid enter their name(or an 
approximation of it).
If you want data about all the children press 'ALL'.
Press 'BLUE', 'GREEN' or 'YELLOW' to get data of each group.
"""

retrieve_recipes = """Retrieve recipes data:

If you want to get a particular recipe enter its name(or an approximation
of if).
For all the recipes data press ALL.
"""

