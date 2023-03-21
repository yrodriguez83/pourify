import csv
import os
import requests

# Set up the API URL to fetch cocktail data
url = 'http://www.thecocktaildb.com/api/json/v1/1/search.php?f=a'

# Make a GET request to the API and parse the JSON response
response = requests.get(url)
data = response.json()

# Open a CSV file to write the data to
csv_filename = 'cocktail_data.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Cocktail Name', 'Ingredients', 'Directions', 'Popularity Rank', 'Cocktail Image URL',
                    'Cocktail Image Path', 'Ingredient Name', 'Ingredient Image URL', 'Ingredient Image Path'])

    # Loop through each cocktail in the response
    for cocktail in data['drinks']:
        # Get the name of the cocktail
        cocktail_name = cocktail['strDrink']

        # Get the ingredients and directions of the cocktail
        cocktail_ingredients = cocktail['strIngredient1']
        for i in range(2, 16):
            ingredient_key = f'strIngredient{i}'
            if cocktail.get(ingredient_key):
                cocktail_ingredients += f', {cocktail[ingredient_key]}'
        cocktail_directions = cocktail['strInstructions']

        # Get the popularity rank of the cocktail
        cocktail_popularity_rank = cocktail['strInstructions']

        # Get the image URL of the cocktail
        cocktail_image_url = cocktail['strDrinkThumb']

        # Download the image of the cocktail
        cocktail_image_filename = f'Cocktail_{cocktail_name}.jpg'
        cocktail_image_path = os.path.join(
            os.getcwd(), cocktail_image_filename)
        with open(cocktail_image_path, mode='wb') as f:
            f.write(requests.get(cocktail_image_url).content)

        # Loop through each ingredient for the current cocktail and get the ingredient name and image URL
        for i in range(1, 16):
            ingredient_key = f'strIngredient{i}'
            if cocktail.get(ingredient_key):
                # Get the name of the ingredient
                ingredient_name = cocktail[ingredient_key]

                # Get the image URL of the ingredient
                ingredient_image_url = f'https://www.thecocktaildb.com/images/ingredients/{ingredient_name.lower()}.png'

                # Download the image of the ingredient
                ingredient_image_filename = f'Ingredient_{ingredient_name}.jpg'
                ingredient_image_path = os.path.join(
                    os.getcwd(), ingredient_image_filename)
                with open(ingredient_image_path, mode='wb') as f:
                    f.write(requests.get(ingredient_image_url).content)

                # Write the data to the CSV file
                writer.writerow([cocktail_name, cocktail_ingredients, cocktail_directions, cocktail_popularity_rank,
                                cocktail_image_url, cocktail_image_path, ingredient_name, ingredient_image_url, ingredient_image_path])
