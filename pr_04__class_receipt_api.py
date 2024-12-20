import requests
import time



def main_menu():
    cooker = SmartCooker()

    while True:
        print("\n1. Найти рецепт")
        print("2. Показать инф. о рецепте")
        print("3. Потовить рецепт")
        print("4. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            query = input("Введите название рецепта для поиска: ")
            recipes_data = RecipeService.find_recipes(query)
            if not recipes_data:
                print("Рецепт не найдены.")
                continue
            print("\nНайденны рецепты:")
            for i, recipe_data in enumerate(recipes_data):
                print(f"{i + 1}. {recipe_data['name']}")

            recipe_index = int(input("Введите номер рецепта, чтобы выбрать его: ")) - 1
            selected_recipe_id = recipes_data[recipe_index]["id"]
            recipe = RecipeService.fetch_recipe_details(selected_recipe_id)
            cooker.load_dish(recipe)

        elif choice == "2":
            cooker.show_recipe_info()

        elif choice == "3":
            cooker.prepare()

        elif choice == "4":
            print("Выход из программы")
            break

        else:
            print("Ошибка выбора. Попробуйте снова")


class CookingPhase:
    def __init__(self, instruction, duration):
        self.instruction = instruction
        self.duration = duration

    def execute(self):
        print(self.instruction)
        time.sleep(self.duration)
class IngredientItem:
    def __init__(self, name, quantity, unit_price):
        self.name = name
        self.quantity = quantity  #кг
        self.unit_price = unit_price

    def calculate_cost(self):
        return self.quantity * self.unit_price

class SmartCooker:
    def __init__(self):
        self.current_recipe = None

    def load_dish(self, recipe):
        self.current_recipe = recipe

    def show_recipe_info(self):
        if self.current_recipe:
            print(f"\nНазвание блюда: {self.current_recipe.title}")
            print(f"Вес сырого продукта: {self.current_recipe.total_raw_weight():.2f} кг")
            print(f"Вес готового продукта: {self.current_recipe.total_cooked_weight():.2f} кг")
            print(f"Себестоимость блюда: {self.current_recipe.calculate_cost_price():.2f} руб")
            print(f"Общее время приготовления: {self.current_recipe.total_preparation_time()} минут\n")
        else:
            print("Рецепт не загружен")

    def prepare(self):
        if not self.current_recipe:
            print("Нет загруженного рецепта")
            return

        print(f"\nНачинаем приготовление блюда: {self.current_recipe.title}\n")
        for step in self.current_recipe.cooking_steps:
            step.execute()
        print("\nПриготовление завершено!\n")


class RecipeService:
    BASE_API_URL = "https://api.spoonacular.com/recipes"
    API_KEY = "c55d1174a17a416f9a5657cd1d1abf16"

    @staticmethod
    def find_recipes(query):
        search_endpoint = f"{RecipeService.BASE_API_URL}/complexSearch"
        params = {
            "query": query,
            "number": 3,
            "apiKey": RecipeService.API_KEY
        }
        response = requests.get(search_endpoint, params=params)
        data = response.json()
        return [{"id": recipe["id"], "name": recipe["title"]} for recipe in data.get("results", [])]

    @staticmethod
    def fetch_recipe_details(recipe_id):
        details_endpoint = f"{RecipeService.BASE_API_URL}/{recipe_id}/information"
        params = {"apiKey": RecipeService.API_KEY}
        response = requests.get(details_endpoint, params=params)
        data = response.json()

        ingredients = [
            {
                "name": ing["name"],
                "quantity": ing["amount"] / 1000,  # перевод в кг
                "unit_price": 100  # условная фиксированная цена (за кг)
            }
            for ing in data.get("extendedIngredients", [])
        ]
        steps = [
            {
                "instruction": step["step"],
                "duration": 5  # интервал
            }
            for step in data.get("analyzedInstructions", [])[0].get("steps", [])
        ]

        return DishRecipe(data["title"], ingredients, steps)

class DishRecipe:
    def __init__(self, title, ingredients_list, cooking_steps):
        self.title = title
        self.ingredients = [IngredientItem(**item) for item in ingredients_list]
        self.cooking_steps = [CookingPhase(**step) for step in cooking_steps]

    def total_raw_weight(self):
        return sum(ingredient.quantity for ingredient in self.ingredients)

    def total_cooked_weight(self):
        return self.total_raw_weight() * 0.9

    def calculate_cost_price(self):

        return sum(ingredient.calculate_cost() for ingredient in self.ingredients)

    def total_preparation_time(self):
        return sum(step.duration for step in self.cooking_steps)


if __name__ == "__main__":
    main_menu()
