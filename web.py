from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

class CocktailDB:
    def __init__(self):
        self.base_url = "https://www.thecocktaildb.com/api/json/v1/1"

    def list_cocktails_by_letter(self, letter):
        search_url = f"{self.base_url}/search.php?f={letter}"
        return self._get_cocktail_names(search_url)

    def list_cocktails_by_ingredient(self, ingredient):
        search_url = f"{self.base_url}/filter.php?i={ingredient}"
        return self._get_cocktail_names(search_url)

    def search_cocktail(self, drink_name):
        search_url = f"{self.base_url}/search.php?s={drink_name}"
        return self._get_cocktail_details(search_url)

    def generate_random_cocktail(self):
        random_cocktail_url = f"{self.base_url}/random.php"
        return self._get_cocktail_details(random_cocktail_url)

    def list_drinks_by_category(self, category):
        search_url = f"{self.base_url}/filter.php?c={category}"
        return self._get_cocktail_details(search_url)

    def _get_cocktail_names(self, url):
        search_data = requests.get(url).json()
        drinks = search_data.get('drinks', [])
        return [drink['strDrink'] for drink in drinks]

    def _get_cocktail_details(self, url):
        cocktail_data = requests.get(url).json()
        cocktail = cocktail_data['drinks'][0] if 'drinks' in cocktail_data else {}
        strDrink = cocktail.get('strDrink', "Unknown Drink")
        ingredients = [cocktail.get(f'strIngredient{i}', '') for i in range(1, 16) if cocktail.get(f'strIngredient{i}', '')]
        return {'strDrink': strDrink, 'ingredients': ', '.join(ingredients)}

class Bartender:
    def list_by_letter(self, letter):
        dallys_bar = CocktailDB()
        cocktail_list = dallys_bar.list_cocktails_by_letter(letter)
        return render_template_string(html_template, letter=letter, cocktail_list=cocktail_list)

    def list_by_ingredient(self, ingredient):
        dallys_bar = CocktailDB()
        cocktail_list = dallys_bar.list_cocktails_by_ingredient(ingredient)
        return render_template_string(html_template, letter=ingredient, cocktail_list=cocktail_list)

    def search(self, drink_name):
        dallys_bar = CocktailDB()
        result = dallys_bar.search_cocktail(drink_name)
        return render_template_string(html_template, letter=drink_name, cocktail_list=[result])

    def random(self):
        dallys_bar = CocktailDB()
        random_result = dallys_bar.generate_random_cocktail()
        return render_template_string(html_template, letter='', cocktail_list=[], result={}, random_result=random_result)

    def list_by_category(self, category):
        dallys_bar = CocktailDB()
        cocktail_list = dallys_bar.list_drinks_by_category(category)
        return render_template_string(html_template, letter=category, cocktail_list=cocktail_list)

    def create_custom_cocktail(self):
        custom_name = request.form["custom_name"]
        custom_ingredients = request.form.getlist("custom_ingredient")
        custom_result = {'strDrink': custom_name, 'ingredients': ', '.join(custom_ingredients)}
        return render_template_string(html_template, letter='', cocktail_list=[], result={}, random_result={}, custom_result=custom_result)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Matt Finnerty Foundation Bartender Tool</title>
    <style>
        body {
            background-color: #333;
            text-align: center;
            font-family: Arial, sans-serif;
            color: #eee;
            margin: 20px;
        }
        h1 {
            color: #007bff;
            margin-bottom: 10px;
        }
        .button-container {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 20px;
        }
        form {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input {
            padding: 8px;
            font-size: 16px;
            width: 200px;
        }
        button {
            padding: 10px;
            background-color: #007bff;
            color: #fff;
            border: none;
            cursor: pointer;
            font-size: 16px;
            border-radius: 5px;
        }
        button:hover {
            background-color: #0056b3;
        }
        .in-memory {
            margin-top: 20px;
            font-style: italic;
            color: #ccc;
        }
        .section-title {
            margin-top: 20px;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            margin-bottom: 5px;
        }
        .result-container {
            background-color: #444;
            padding: 10px;
            border-radius: 5px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>The Matt Finnerty Foundation Bartender Tool</h1>
    <div class="button-container">
        <form method="post" action="/list_by_letter">
            <label for="letter">Enter the first letter of a cocktail:</label>
            <input type="text" id="letter" name="letter" required>
            <button type="submit">List by Letter</button>
        </form>

        <form method="post" action="/list_by_ingredient">
            <label for="ingredient">Enter an ingredient to search by:</label>
            <input type="text" id="ingredient" name="ingredient" required>
            <button type="submit">List by Ingredient</button>
        </form>

        <form method="post" action="/search">
            <label for="drink_name">Enter the name of the drink:</label>
            <input type="text" id="drink_name" name="drink_name" required>
            <button type="submit">Search Drink</button>
        </form>

        <form method="post" action="/random">
            <button type="submit">Generate Random Drink</button>
        </form>
        
        <form method="post" action="/list_by_category">
            <label for="category">Enter a category to search by:</label>
            <input type="text" id="category" name="category" required>
            <button type="submit">List by Category</button>
        </form>

        <form method="post" action="/create_custom_cocktail">
            <button type="submit">Create Custom Cocktail</button>
        </form>
    </div>

    <div class="in-memory">In loving memory of Matt Finnerty who was loathed by all</div>

    {% if letter %}
        <h2 class="section-title">Drinks found by the query: '{{ letter }}'</h2>
        {% if cocktail_list %}
            <ul>
                {% for cocktail in cocktail_list %}
                    <li>{{ cocktail }}</li>
                {% endfor %}
            </ul>
        {% else %}
            <p>No cocktails found with the letter '{{ letter }}'</p>
        {% endif %}
    {% endif %}

    {% if result %}
        <div class="result-container">
            <h2 class="section-title">{{ result['strDrink'] }}</h2>
            <p>Ingredients: {{ result['ingredients'] }}</p>
        </div>
    {% endif %}

    {% if random_result %}
        <div class="result-container">
            <h2 class="section-title">{{ random_result['strDrink'] }}</h2>
            <p>Ingredients: {{ random_result['ingredients'] }}</p>
        </div>
    {% endif %}
</body>
</html>
"""
@app.route('/list_by_letter', methods=['POST'])
def list_by_letter():
    letter = request.form['letter']
    bartender = Bartender()
    return bartender.list_by_letter(letter)

@app.route('/list_by_ingredient', methods=['POST'])
def list_by_ingredient():
    ingredient = request.form['ingredient']
    bartender = Bartender()
    return bartender.list_by_ingredient(ingredient)

@app.route('/search', methods=['POST'])
def search():
    drink_name = request.form['drink_name']
    bartender = Bartender()
    return bartender.search(drink_name)

@app.route('/random', methods=['POST'])
def random():
    bartender = Bartender()
    return bartender.random()

@app.route('/list_by_category', methods=['POST'])
def list_by_category():
    category = request.form['category']
    bartender = Bartender()
    return bartender.list_by_category(category)

@app.route('/create_custom_cocktail', methods=['POST'])
def create_custom_cocktail():
    bartender = Bartender()
    return bartender.create_custom_cocktail()

@app.route('/')
def index():
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)