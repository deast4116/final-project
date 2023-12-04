import json
import requests
class bar:
#change init and str to not include the search method as well as ask user which methods they want to use, add the ability to obtain ingredients list as well as recipie,
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

    def generate_random_cocktail(self):
        random_cocktail_url = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
        random_cocktail_data = requests.get(random_cocktail_url).json()
        cocktail = random_cocktail_data['drinks'][0] if 'drinks' in random_cocktail_data else {}
        strDrink = cocktail.get('strDrink', "Unknown Drink")
        return f"Generated Drink: {strDrink}"

        "Encountered a significant problem here that's entirely out of my control."
        "The database on occasion will return a drink that has yet to be finished resulting in- "
        "An error. I made a way around it however this still shouldn't be possible and was frustrating to work around"


    def list_cocktails_by_letter(self, letter):
        search_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}"
        search_data = requests.get(search_url).json()
        drinks = search_data.get('drinks', [])
        drink_names = [drink['strDrink'] for drink in drinks]
        return drink_names


def main():
    drink_to_search = input("What drink are you lookin' for pardner?: ")
    dallys_bar = bar(drink_to_search)

    print("I found this:")
    print(str(dallys_bar))
    print("Random drink of the night (or day I don't judge) is:")
    print(dallys_bar.generate_random_cocktail())

    letter = input("Enter the first letter of a cocktail yer' lookin' for to see if we have it: ")
    print("Cocktails by that letter are:")
    print(dallys_bar.list_cocktails_by_letter(letter))

main()