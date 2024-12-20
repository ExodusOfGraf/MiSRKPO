import time
#Фамилия = Графсков. Выбранное блюдо = Грушевый пирог

# (Г)рафсков -> (Г)рушевый пирог

class Ingredient:
    def __init__(self, name, weight, price_per_kg):
        self.name = name
        self.weight = weight
        self.price_per_kg = price_per_kg

    def cost(self):
        return self.weight * self.price_per_kg


class Step:
    def __init__(self, description, time_to_next):
        self.description = description
        self.time_to_next = time_to_next


class Recipi:
    def __init__(self, name, ingredients, steps):
        self.name = name
        self.ingredients = [Ingredient(*ing) for ing in ingredients]
        self.steps = [Step(*step) for step in steps]

    def raw_weight(self):
        return sum(ingredient.weight for ingredient in self.ingredients)

    def cooked_weight(self):
        return self.raw_weight() * 0.9  # условная потеря в весе = 10%

    def cost(self):
        return sum(ingredient.cost() for ingredient in self.ingredients)

    def total_cooking_time(self):
        return sum(step.time_to_next for step in self.steps)




class Cooker:
    def __init__(self, recipe):
        self.recipe = recipe

    def prepare(self, quantity=1):
        print(f"Приготовление блюда '{self.recipe.name}'...")
        for _ in range(quantity):
            for step in self.recipe.steps:
                print(step.description)
                time.sleep(step.time_to_next)
            print("Блюдо готово!\n")
recipe_data = {
    "name": "Грушевый пирог",
    "ingredients": [
        ("груша", 0.5, 120.0),
        ("сахар", 0.1, 50.0),
        ("мука", 0.3, 40.0),
        ("масло сливочное", 0.1, 90.0),
        ("яйцо", 0.1, 60.0)
    ],
    "steps": [
        ("Подготовить все ингредиенты.", 2),
        ("Смешать муку и сахар.", 1),
        ("Добавить масло и взбитое яйцо.", 2),
        ("Положить нарезанную грушу.", 1),
        ("Выпекать 30 минут при 180 градусах.", 30)
    ]
}

recipe = Recipi(recipe_data["name"], recipe_data["ingredients"], recipe_data["steps"])
cooker = Cooker(recipe)
# Самопров.
print("Вес сырого продукта:", recipe.raw_weight(), "кг")
print("Вес готового продукта:", recipe.cooked_weight(), "кг")
print("Себестоимость блюда:", recipe.cost(), "руб.")
print("Общее время приготовления:", recipe.total_cooking_time(), "минут")

# Симуляция/
cooker.prepare(quantity=1)

