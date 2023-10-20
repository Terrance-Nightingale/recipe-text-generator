import os
import string
import pandas as pd
import requests


class Cookbook:

    def __init__(self):
        self.username = os.environ['USERNAME']
        self.apikey = os.environ['APIKEY']
        self.hash = os.environ['HASH']
        self.recipes = []
        self.shopping_list = []

        self.header = {
            "Content-Type": "application/json"
        }

    def get_recipes(self):
        url = "https://api.spoonacular.com/mealplanner/generate"
        parameters = {
            "username": self.username,
            "hash": self.hash,
            "apiKey": self.apikey,
            "timeFrame": "week"
        }
        response = requests.get(url=url, params=parameters, headers=self.header)
        data = response.json()
        for day in data['week']:
            for recipe in data['week'][f'{day}']['meals']:
                recipe_to_add = {
                    "ID": recipe['id'],
                    "Day": day.capitalize(),
                    "Name": recipe['title'],
                    "URL": recipe['sourceUrl']
                }
                self.recipes.append(recipe_to_add)
        return self.recipes

    def get_shopping_list(self):
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
        shop_df = pd.DataFrame(self.shopping_list)
        recipe_df = pd.DataFrame(self.recipes)

        all_dfs = [
            shop_df,
            recipe_df
        ]

        agg_criteria = {
            'Ingredient': 'first',
            'Amount': 'sum',
            'Unit': 'first'
        }
        agg_shop = shop_df.groupby(['Ingredient']).agg(agg_criteria)

        d = dict(zip(range(26), list(string.ascii_uppercase)))

        with pd.ExcelWriter("shopping_list.xlsx") as writer:
            recipe_df.to_excel(writer, sheet_name="Recipes_This_Week", index=False)
            agg_shop.to_excel(writer, sheet_name="Shopping_List", index=False)

            workbook = writer.book
            wrap_format = workbook.add_format({'text_wrap': True})

            for sheet in writer.sheets:
                worksheet = writer.sheets[sheet]
                for df in all_dfs:
                    for col in df.columns:
                        worksheet.set_column(col, None, wrap_format)
