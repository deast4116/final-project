import json
import requests
class ListBarClass:
    def __init__(self):
        pass

    def list_drinks_by_letter(self):
        letter = input("Enter the first letter of a cocktail: ")
        search_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}"
        search_data = requests.get(search_url).json()
        drinks = search_data.get('drinks', [])
        drink_names = [drink['strDrink'] for drink in drinks]
        return drink_names

    def list_drinks_by_ingredient(self):
        ingredient = input("Enter an ingredient to search by: ")
        search_url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ingredient}"
        search_data = requests.get(search_url).json()
        drinks = search_data.get('drinks', [])
        drink_names = [drink['strDrink'] for drink in drinks]
        return drink_names


class SearchBarClass:
    def __init__(self):
        pass

    def search_all_drinks(self):
        drink_name = input("Enter the name of the drink: ")
        search_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink_name}"
        search_data = requests.get(search_url).json()
        drinks = search_data.get('drinks', [])
        if drinks:
            drink = drinks[0]
            ingredients = [drink.get(f'strIngredient{i}', '') for i in range(1, 16) if drink.get(f'strIngredient{i}', '')]
            return f"Drink: {drink['strDrink']}\nIngredients: {', '.join(ingredients)}"
        else:
            return "Drink not found."

    def generate_random_drink(self):
        random_cocktail_url = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
        random_cocktail_data = requests.get(random_cocktail_url).json()
        cocktail = random_cocktail_data['drinks'][0] if 'drinks' in random_cocktail_data else {}
        strDrink = cocktail.get('strDrink', "Unknown Drink")
        ingredients = [cocktail.get(f'strIngredient{i}', '') for i in range(1, 16) if cocktail.get(f'strIngredient{i}', '')]
        return f"Generated Drink: {strDrink}\nIngredients: {', '.join(ingredients)}"

def main():
    list_bar = ListBarClass()
    search_bar = SearchBarClass()
    drinks_by_letter = list_bar.list_drinks_by_letter()
    print("Cocktails by letter:", drinks_by_letter)

    drinks_by_ingredient = list_bar.list_drinks_by_ingredient()
    print("Cocktails by ingredient:", drinks_by_ingredient)

    searched_drink = search_bar.search_all_drinks()
    print(searched_drink)

    random_drink = search_bar.generate_random_drink()
    print(random_drink)

main()