import os
import pandas as pd
import requests


class Cookbook:

    def __init__(self):
        # Authentication variables. A Spoonacular account is needed to obtain these.
        self.username = os.environ['USERNAME']
        self.apikey = os.environ['APIKEY']
        self.hash = os.environ['HASH']

        # These variables are populated by calling the Cookbook class's related methods.
        self.recipes = []
        self.shopping_list = []

        # Header for all Spoonacular requests.
        self.header = {
            "Content-Type": "application/json"
        }

    def get_recipes(self):
        """
        Pulls three recipes from Spoonacular API for each day of the week, then populates and returns self.recipes.

        """
        url = "https://api.spoonacular.com/mealplanner/generate"
        parameters = {
            "username": self.username,
            "hash": self.hash,
            "apiKey": self.apikey,
            "timeFrame": "week"
        }
        response = requests.get(url=url, params=parameters, headers=self.header)
        data = response.json()
        try:
            for day in data['week']:
                for recipe in data['week'][f'{day}']['meals']:
                    recipe_to_add = {
                        "ID": recipe['id'],
                        "Day": day.capitalize(),
                        "Name": recipe['title'],
                        "URL": recipe['sourceUrl']
                    }
                    self.recipes.append(recipe_to_add)
        except KeyError:
            raise KeyError("You've used up your Spoonacular API quota for the day. Please try again tomorrow.")
        return self.recipes

    def get_shopping_list(self):
        """
        Pulls ingredient information based on the ids of the meals pulled in get_recipes,
        then populates and returns self.shopping_list.
        """
        url = "https://api.spoonacular.com/recipes/informationBulk"
        ids = ""
        for recipe in self.recipes:
            id_to_ad = f"{recipe['ID']},"
            ids += id_to_ad
        parameters = {
            "username": self.username,
            "hash": self.hash,
            "apiKey": self.apikey,
            "ids": ids
        }
        response = requests.get(url=url, params=parameters, headers=self.header)
        data = response.json()
        for recipe in data:
            for ingredient in recipe['extendedIngredients']:
                if ingredient['nameClean'] is not None:
                    new_item = {
                        "Ingredient": ingredient['nameClean'],
                        "Amount": ingredient['measures']['us']['amount'],
                        "Unit": ingredient['measures']['us']['unitShort']
                    }
                else:
                    new_item = {
                        "Ingredient": ingredient['name'],
                        "Amount": round(float(ingredient['measures']['us']['amount']), 2),
                        "Unit": ingredient['measures']['us']['unitShort']
                    }
                self.shopping_list.append(new_item)
        return self.shopping_list

    def save_recipes(self):
        """
        Saves the recipes and shopping list in Cookbook as Excel files (.xlsx).
        """
        shop_df = pd.DataFrame(self.shopping_list)
        recipe_df = pd.DataFrame(self.recipes)

        # Aggregates any rows in the shopping list where the ingredients are the same.
        agg_criteria = {
            'Ingredient': 'first',
            'Amount': 'sum',
            'Unit': 'first'
        }
        agg_shop = shop_df.groupby(['Ingredient']).agg(agg_criteria)

        all_dfs = [
            agg_shop,
            recipe_df
        ]

        # Sets file path to desktop regardless of user.
        path = os.path.join(os.path.expanduser("~"), "Desktop", "shopping_list.xlsx")
        with pd.ExcelWriter(path) as writer:
            recipe_df.to_excel(writer, sheet_name="Recipes_This_Week", index=False)
            agg_shop.to_excel(writer, sheet_name="Shopping_List", index=False)

            workbook = writer.book
            wrap_format = workbook.add_format({'text_wrap': True})

            for sheet in writer.sheets:
                worksheet = writer.sheets[sheet]
                for df in all_dfs:
                    total_col = len(df.columns)
                    worksheet.set_column(0, total_col, 20, wrap_format)
