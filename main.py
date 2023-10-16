from text_send import TextSender
from recipe_generator import Cookbook

# TODO Compile recipes into SMS message to send to user
# TODO Connect to Windows Task Manager to automate process every Friday at noon

body = "This is a separate test of the body system."

texter = TextSender()
cookbook = Cookbook()

# texter.send_text(body=body)
recipes = cookbook.get_recipes()
shopping_list = cookbook.get_shopping_list()
print(shopping_list)
