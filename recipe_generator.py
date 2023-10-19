import os
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
                new_item = {
                    "Ingredient": ingredient['originalName'],
                    "Amount": ingredient['measures']['us']['amount'],
                    "Unit": ingredient['measures']['us']['unitShort']
                }
                self.shopping_list.append(new_item)
        return self.shopping_list
