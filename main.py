from text_send import TextSender
from recipe_generator import Cookbook

# TODO Compile recipes into SMS message to send to user
# TODO Connect to Windows Task Manager to automate process every Friday at noon

body = "This is a test."

texter = TextSender()
cookbook = Cookbook()

recipes = cookbook.get_recipes()
shopping_list = cookbook.get_shopping_list()
# texter.send_text(body=body)
