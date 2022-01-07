# Daily Manu APP

The main goal of this app is to create a daily menu for a group of kids. The user can create kids and recipes data, then choose a group of kids or all of them and choose a recipe to create a daily menu.

When a kid is created, a list of allergies can be created if the kid has one or more.
Then, this list is compared against the ingredients of a recipe chosen, and if the kid is allergic to an ingredient, the user is alerted and they can choose another recipe for that kid.

## Features

### Welcome to the app

The first screen that the user sees is a welcome with a little explanation about the app and the main menu. 

They can choose to create a menu, retrieve data, create data, get some help or leave the app. 

![Image](images/readme/welcome.png)

### Help

Here the user can get a deeper explanation about the app.

![Image](images/readme/help.png)

### Cretae a menu

When the user enters the daily menu option, a screen is displayed indicating if a menu has already been created. If no menu has been created yet, the screen is as follows.

![Image](images/readme/daily_no_created.png)

The user can choose to create a daily menu for a specific group or for all the children.

A list of all the recipes is displayed for the user choose one of them by its id.

This screen is shown when an user choose to create a menu for a specific group. A menu is already created in this screenshot.

![Image](images/readme/create_menu_1.png)

Once the user has chosen a recipe, if one or more kids are allergic to it, the user must choose another recipe for them.

![Image](images/readme/create_menu_2.png)

![Image](images/readme/create_menu_3.png)

When all the kids have an assign recipe, every recipe chosen is show as well as the rations of each of them that have to be prepared.

![Image](images/readme/create_menu_4.png)

From the daily menu panel the user can see which are the menus that have been already created. 

![Image](images/readme/daily_menu_1.png)

The user can update a menu if it is already created and the old menu will be replaced by the new one.

![Image](images/readme/update_menu.png)

### Retrieve data

The user can retrieve data about kids grouping them by group, all of them or just one kid and data about one recipe or all of them as well.

![Image](images/readme/retrieve_data_1.png)

In case there is a coincidence in the params of search, the user must choice an option choosing it by id.

![Image](images/readme/object_coincidence_chosen.png)

### Create data

The user can create kid and recipes data. The app will guide them asking for all the data needed to create each one of them.

Every field to fill has its validator and an alert will be show to user in case they enter the wrong data.

![Image](images/readme/enter_incorrect_data.png)

When the data is saved a message is shown to the user

![Image](images/readme/create_data_1.png)

## Features left to implement

A nice feature would be to create a weekly menu, where the user could create a menu for every day of the week.

Another interesting feature would be to have the possibility to add quantity of each ingredient in a recipe, in grams or units, so that each recipe has a total amount of weight or units of ingredients, then a purchase list can be created from those ingredients for each recipe for the day or the week if the weekly menu had been implemented.

## Testing

## Bugs

When a kid had more than one allergy to a recipe, they was counted as a different child as many time as there were allergies.

I fixed it adding a condition to the loop in which the allergic kids were counted: 

![Image](images/readme/bugs/kid_more_than_one_allergy.png)

When I had two or more different allergy recipes and loaded them into the worksheet, only one would be saved. That was because I was rewriting the object.

In fact, I was making the code more complicated than it should be. The final code is as follow:

![Image](images/readme/bugs/allergic_recipes_fixed.png)

## Deployment

### The app has been deployed in Heroku.

First of all I had to create or in this case update a file with the needed requirements to the app works. It says to Heroku which dependencies are necessary to be implemented.

To do that I used the command `pip3 freeze --local > requirements.txt` . I had use first just `pip3 freeze > requirements.txt` but it didn't work.

Then I pushed the code to github and create a Heroku account. Create an account is very easy, just register the email and follow the tipical steps to finish the registration.

In Heroku I had to create a new app, give it a name and choosing a region.

Once the app is created, I went to setting, in config vars configuration, I setted the environment variables that were two, CREDS = creas.json and PORT = 8000.

Next step is to add two buildpacks, Python and Node. In that order. That is very important.

Then I went to deploy section and connect the app with the github repository. There are two ways to connect it with github, enable automatics deploys if we want to every time we push a commit the app automatically rebuild or manually deploy which was what I used this time.

After this if there is no problem with the code, the app will be build.

[The app is runnig here](https://ale-daily-menu.herokuapp.com/)



