from text_send import TextSender
from recipe_generator import Cookbook

# Creates classes that will gather weekly meal info and notify the user by text.
texter = TextSender()
cookbook = Cookbook()

# Gets recipes and corresponding shopping list
cookbook.get_recipes()
cookbook.get_shopping_list()
cookbook.save_recipes()

# Sets the body of the text and sends it.
body = "This week's meals have been generated and saved to your desktop as \"shopping_list.xlsx\". " \
       "Open the file to view your recipes and shopping list for the week!"
texter.send_text(body=body)
