from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)


class Bar:
    def __init__(self, drink_to_search):
        self.drink_to_search = drink_to_search

    def list_cocktails_by_letter(self, letter):
        search_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}"
        search_data = requests.get(search_url).json()
        if 'drinks' in search_data:
            drinks = search_data['drinks']
            drink_names = [drink['strDrink'] for drink in drinks]
            return drink_names
        else:
            return []

    def list_cocktails_by_ingredient(self, ingredient):
        search_url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ingredient}"
        search_data = requests.get(search_url).json()
        drinks = search_data.get('drinks', [])
        drink_names = [drink['strDrink'] for drink in drinks]
        return drink_names

    def search_cocktail(self, drink_name):
        search_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink_name}"
        search_data = requests.get(search_url).json()
        drinks = search_data.get('drinks', [])
        if drinks:
            drink = drinks[0]
            ingredients = [drink.get(f'strIngredient{i}', '') for i in range(1, 16) if
                           drink.get(f'strIngredient{i}', '')]
            return f"Drink: {drink['strDrink']}\nIngredients: {', '.join(ingredients)}"
        else:
            return "Drink not found."

    def generate_random_cocktail(self):
        random_cocktail_url = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
        random_cocktail_data = requests.get(random_cocktail_url).json()
        cocktail = random_cocktail_data['drinks'][0] if 'drinks' in random_cocktail_data else {}
        strDrink = cocktail.get('strDrink', "Unknown Drink")
        ingredients = [cocktail.get(f'strIngredient{i}', '') for i in range(1, 16) if
                       cocktail.get(f'strIngredient{i}', '')]
        return f"Generated Drink: {strDrink}\nIngredients: {', '.join(ingredients)}"


html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dafek's Abode</title>
    <style>
        body {
            background-color: #f5f5f5;
            text-align: center;
            font-family: Arial, sans-serif;
            color: #333;
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
            color: #555;
        }
        .section-title {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Welcome to Dafek's Abode</h1>
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
    </div>

    <div class="in-memory">In loving memory of Matt Finnerty</div>
    
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
</body>
</html>
"""

@app.route('/list_by_letter', methods=['POST'])
def list_by_letter():
    letter = request.form['letter']
    dallys_bar = Bar(letter)
    cocktail_list = dallys_bar.list_cocktails_by_letter(letter)
    return render_template_string(html_template, letter=letter, cocktail_list=cocktail_list)

@app.route('/list_by_ingredient', methods=['POST'])
def list_by_ingredient():
    ingredient = request.form['ingredient']
    dallys_bar = Bar('')
    cocktail_list = dallys_bar.list_cocktails_by_ingredient(ingredient)
    return render_template_string(html_template, letter=ingredient, cocktail_list=cocktail_list)

@app.route('/search', methods=['POST'])
def search():
    drink_name = request.form['drink_name']
    dallys_bar = Bar('')
    result = dallys_bar.search_cocktail(drink_name)
    return render_template_string(html_template, letter=drink_name, cocktail_list=[result])

@app.route('/random', methods=['POST'])
def random():
    dallys_bar = Bar('')
    result = dallys_bar.generate_random_cocktail()
    return render_template_string(html_template, letter='', cocktail_list=[result])

@app.route('/')
def index():
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)