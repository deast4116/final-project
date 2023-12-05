from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)


class Bar:
    def __init__(self, drink_to_search):
        self.api_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink_to_search}"
        self.drink_data_dict = requests.get(self.api_url).json()
        self.drink_to_search = drink_to_search

    def __str__(self):
        drinks = self.drink_data_dict['drinks']
        if drinks:
            return f"Drinks found in the database that match your search:'{self.drink_to_search}':\n{', '.join(drink['strDrink'] for drink in drinks)}"
        else:
            return f"No drinks found under the name '{self.drink_to_search}'."

    def list_cocktails_by_letter(self, letter):
        search_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}"
        search_data = requests.get(search_url).json()
        drinks = search_data.get('drinks', [])
        drink_names = [drink['strDrink'] for drink in drinks]
        return drink_names


html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drink Search</title>
</head>
<body>
    <h1>Welcome to Dally's Bar</h1>
    <form method="post" action="/">
        <label for="letter">Enter the first letter of a cocktail:</label>
        <input type="text" id="letter" name="letter" required>
        <button type="submit">Search</button>
    </form>
    {% if letter %}
        <h2>Cocktails with the letter '{{ letter }}'</h2>
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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        letter = request.form['letter']
        dallys_bar = Bar(letter)
        cocktail_list = dallys_bar.list_cocktails_by_letter(letter)
        return render_template_string(html_template, letter=letter, cocktail_list=cocktail_list)
    return render_template_string(html_template)


if __name__ == '__main__':
    app.run(debug=True)
