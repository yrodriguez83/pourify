import csv
import requests
from pymongo import MongoClient


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
