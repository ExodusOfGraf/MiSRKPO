import requests
import time

# Класс Ингредиент
class Ingredient:
    def __init__(self, name, weight, price_per_kg):
        self.name = name  
        self.weight = weight  # Вес в кг
        self.price_per_kg = price_per_kg  # Цена за кг

    def cost(self):
        """Вычисляем стоимость ингредиента."""
        return self.weight * self.price_per_kg


# Класс Этап Приготовления
class CookingStep:
    def __init__(self, description, time_to_next):
        self.description = description  
        self.time_to_next = time_to_next 

    def perform(self):
        print(self.description)
        time.sleep(self.time_to_next)


# Класс Рецепт
class Recipe:
    def __init__(self, name, ingredients, steps):
        self.name = name  
        self.ingredients = [Ingredient(**ing) for ing in ingredients]  
        self.steps = [CookingStep(**step) for step in steps]  

    def raw_weight(self):
        """Считаем общий вес всех ингредиентов."""
        return sum(ingredient.weight for ingredient in self.ingredients)

    def cooked_weight(self):
        """Считаем вес готового продукта (примерно 90% от сырого веса)."""
        return self.raw_weight() * 0.9

    def cost_price(self):
        """Считаем себестоимость блюда."""
        return sum(ingredient.cost() for ingredient in self.ingredients)

    def total_cooking_time(self):
        """Считаем общее время приготовления на основе всех этапов."""
        return sum(step.time_to_next for step in self.steps)


# Класс Автоматический Приготовитель
class AutomaticCooker:
    def __init__(self):
        self.recipe = None  
        self.favorite_recipes = []

    def load_recipe(self, recipe):
        self.recipe = recipe

    def display_info(self):
        """Выводит информацию о весе, стоимости и времени приготовления."""
        if self.recipe:
            print(f"\nНазвание блюда: {self.recipe.name}")
            print(f"Вес сырого продукта: {self.recipe.raw_weight():.2f} кг")
            print(f"Вес готового продукта: {self.recipe.cooked_weight():.2f} кг")
            print(f"Себестоимость блюда: {self.recipe.cost_price():.2f} руб")
            print(f"Общее время приготовления: {self.recipe.total_cooking_time()} минут\n")
        else:
            print("Рецепт не загружен.")

    def cook(self):
        """Процесс приготовления, вывод шагов с паузами."""
        if not self.recipe:
            print("Нет загруженного рецепта.")
            return

        print(f"\nНачинаем приготовление блюда: {self.recipe.name}\n")
        for step in self.recipe.steps:
            step.perform()
        print("\nПриготовление завершено!\n")

    def add_to_favorites(self):
        """Добавляет текущий рецепт в список понравившихся."""
        if self.recipe and self.recipe not in self.favorite_recipes:
            self.favorite_recipes.append(self.recipe)
            print(f"Рецепт '{self.recipe.name}' добавлен в понравившиеся.")
        else:
            print("Рецепт уже добавлен в понравившиеся или не выбран.")

    def show_favorites(self):
        """Выводит список понравившихся рецептов."""
        if not self.favorite_recipes:
            print("Нет понравившихся рецептов.")
            return

        print("\nПонравившиеся рецепты:")
        for i, recipe in enumerate(self.favorite_recipes):
            print(f"{i + 1}. {recipe.name}")

    def choose_from_favorites(self):
        """Позволяет выбрать и загрузить понравившийся рецепт."""
        if not self.favorite_recipes:
            print("Список понравившихся рецептов пуст.")
            return

        self.show_favorites()
        choice = int(input("Введите номер рецепта для загрузки: ")) - 1
        if 0 <= choice < len(self.favorite_recipes):
            self.recipe = self.favorite_recipes[choice]
            print(f"Рецепт '{self.recipe.name}' загружен.")
        else:
            print("Неверный номер рецепта.")


class RecipeAPI:
    BASE_URL = "https://api.spoonacular.com/recipes"
    API_KEY = "f796b0e53f854368888919d38a690987"

    @staticmethod
    def search_recipes(query):
        search_url = f"{RecipeAPI.BASE_URL}/complexSearch"
        params = {
            "query": query,
            "number": 3,
            "apiKey": RecipeAPI.API_KEY
        }
        response = requests.get(search_url, params=params)
        data = response.json()
        return [{"id": recipe["id"], "name": recipe["title"]} for recipe in data.get("results", [])]

    @staticmethod
    def get_recipe_details(recipe_id):
        details_url = f"{RecipeAPI.BASE_URL}/{recipe_id}/information"
        params = {"apiKey": RecipeAPI.API_KEY}
        response = requests.get(details_url, params=params)
        data = response.json()

        ingredients = [
            {
                "name": ing["name"],
                "weight": ing["amount"] / 1000,  
                "price_per_kg": 100  
            }
            for ing in data.get("extendedIngredients", [])
        ]
        steps = [
            {
                "description": step["step"],
                "time_to_next": 5  
            }
            for step in data.get("analyzedInstructions", [])[0].get("steps", [])
        ]

        return Recipe(data["title"], ingredients, steps)


# Основное меню консольного приложения
def main():
    cooker = AutomaticCooker()

    while True:
        print("\n1. Найти рецепт")
        print("2. Показать информацию о рецепте")
        print("3. Готовить рецепт")
        print("4. Добавить рецепт в понравившиеся")
        print("5. Показать понравившиеся рецепты")
        print("6. Выбрать рецепт из понравившихся")
        print("7. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            query = input("Введите название рецепта для поиска: ")
            recipes_data = RecipeAPI.search_recipes(query)
            if not recipes_data:
                print("Рецепты не найдены.")
                continue
            print("\nНайденные рецепты:")
            for i, recipe_data in enumerate(recipes_data):
                print(f"{i + 1}. {recipe_data['name']}")

            recipe_index = int(input("Введите номер рецепта, чтобы выбрать его: ")) - 1
            selected_recipe_id = recipes_data[recipe_index]["id"]
            recipe = RecipeAPI.get_recipe_details(selected_recipe_id)
            cooker.load_recipe(recipe)

        elif choice == "2":
            cooker.display_info()

        elif choice == "3":
            cooker.cook()

        elif choice == "4":
            cooker.add_to_favorites()

        elif choice == "5":
            cooker.show_favorites()

        elif choice == "6":
            cooker.choose_from_favorites()

        elif choice == "7":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
