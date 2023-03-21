import csv
import requests
from pymongo import MongoClient

# Define the URLs of the raw data files
COCkTAILS_URL = "https://example.com/cocktails.csv"
INGREDIENTS_URL = "https://example.com/ingredients.csv"

# Define the database connection parameters
DB_NAME = "cocktail_recipes"
DB_HOST = "localhost"
DB_PORT = 27017

# Connect to the database
client = MongoClient(DB_HOST, DB_PORT)
db = client[DB_NAME]

# Define the data models for the application


class Cocktail:
    def __init__(self, name, image_url, ingredients):
        self.name = name
        self.image_url = image_url
        self.ingredients = ingredients


class Ingredient:
    def __init__(self, name, unit, category):
        self.name = name
        self.unit = unit
        self.category = category


# Collect and process the raw cocktail data
cocktail_data = []
with requests.get(COCKTAILS_URL) as r:
    reader = csv.DictReader(r.content.decode('utf-8').splitlines())
    for row in reader:
        name = row["name"]
        image_url = row["image_url"]
        ingredient_names = row["ingredients"].split(", ")
        ingredients = []
        for ingredient_name in ingredient_names:
            ingredient = db.ingredients.find_one({"name": ingredient_name})
            if not ingredient:
                ingredient = Ingredient(
                    name=ingredient_name, unit="", category="")
                db.ingredients.insert_one(ingredient.__dict__)
            ingredients.append(ingredient.__dict__)
        cocktail = Cocktail(name=name, image_url=image_url,
                            ingredients=ingredients)
        cocktail_data.append(cocktail.__dict__)

# Collect and process the raw ingredient data
ingredient_data = []
with requests.get(INGREDIENTS_URL) as r:
    reader = csv.DictReader(r.content.decode('utf-8').splitlines())
    for row in reader:
        name = row["name"]
        unit = row["unit"]
        category = row["category"]
        ingredient = Ingredient(name=name, unit=unit, category=category)
        ingredient_data.append(ingredient.__dict__)

# Store the processed data in the database
db.cocktails.insert_many(cocktail_data)
db.ingredients.insert_many(ingredient_data)
