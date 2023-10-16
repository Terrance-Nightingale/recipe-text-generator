import os
import requests


class Cookbook:

    def __init__(self):
        self.header = {
            "Content-Type": "application/json"
        }
        self.username = os.environ['USERNAME']
        self.hash = os.environ['HASH']
        self.apikey = os.environ['APIKEY']

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
        recipes = []
        for day in data['week']:
            for recipe in data['week'][f'{day}']['meals']:
                recipe_to_add = {
                    "Day": day.capitalize(),
                    "Name": recipe['title'],
                    "URL": recipe['sourceUrl']
                }
                recipes.append(recipe_to_add)
        return recipes

    def get_shopping_list(self):
        url = f"https://api.spoonacular.com/mealplanner/{self.username}/shopping-list"
        parameters = {
            "username": self.username,
            "hash": self.hash,
            "apiKey": self.apikey
        }
        response = requests.get(url=url, params=parameters, headers=self.header)
        data = response.json()
        print(data)
        shopping_list = []
        for aisle in data["aisles"]:
            for item in aisle["items"]:
                item_to_buy = {
                    "Name": item["name"],
                    "Amount": item["measures"]["original"]["amount"],
                    "Unit": item["measures"]["original"]["unit"]
                }
                shopping_list.append(item_to_buy)
        return shopping_list
