"""Практическая работа №2."""

# Вводная часть
# -------------

"""
В классе могут быть как атрибуты самого класса, так и атрибуты каждого экземпляра объекта.
Задание позволит проанализировать отличие их на практике.
А также закрепить понятия абстракции, полиморфизма, инкапсуляции и наследования на практике.
"""

# Задание
# ----------

"""
Задание открытое, но следует написать python-код так, чтобы выполнялись следующие минимальные условия:

- был класс родитель и два наследуемого от него класса
- название класса-родителя (или одного из наследников) - это название растения/животного/птицы/рыбы и т.п.,
  которое начинается с тойже буквы, что и фамилия студента (должно быть указано в начале файла)

- в классе-родителе:
    - задан классовый атрибут, как константа (неизменяемый)
    - задан приватный классовый атрибут, как аккумулятор объектов (изменяемый)
    - в инициализаторе задан хотя бы один параметр
    - объявлены абстрактные методы (2+)
    - объявлен метод, который выводит количество созданных объектов того или иного типа (тип:количество)
- в классах-наследниках:
    - реализованы абстрактные методы
    - в одном из наследников константному атрибуту задано другое значение
    - реализован метод __str__(), дающий полное представление об основных характеристиках экземпляра
- названия атрибутов и методов названы по их назначению

"""


from abc import ABC, abstractmethod

# Графсков, фамилия начинается с Г, я выбрал животное "Гепард"
class Gepard(ABC):  # Родительский класс
    LEGS_CNT = 4  # Классовый атрибут-константа
    __count = 0  # Приватный классовый атрибут - аккумулятор объектов

    def __init__(self, speed):
        self.__speed = speed  # Пример инкапсуляции, защищённый атрибут
        Gepard.__count += 1  # Увеличиваем количество объектов при создании

    @abstractmethod
    def hunt(self, distance):
        pass

    @abstractmethod
    def rest(self, duration):
        pass

    @classmethod
    def get_object_count(cls):
        return f"Всего объектов Gepard: {cls.__count}"

    def __str__(self):
        return f"Гепард со скоростью: {self.__speed} км/ч"


class FastGepard(Gepard):  # Наследник
    LEGS_CNT = 3  # Изменение значения константного атрибута

    def __init__(self, speed):
        super().__init__(speed)

    def hunt(self, distance):
        return f"FastGepard может охотиться {distance} км."

    def rest(self, duration):
        return f"FastGepard отдыхает {duration} часов."

    def __str__(self):
        return f"FastGepard имеет скорость: {self._Gepard__speed} км в час и {self.LEGS_CNT} лап"


class StrongGepard(Gepard):  # Наследник
    def __init__(self, speed):
        super().__init__(speed)

    def hunt(self, distance):
        return f"StrongGepard может охотиться {distance} километров"

    def rest(self, duration):
        return f"StrongGepard отдыхает {duration} часов"

    def __str__(self):
        return f"StrongGepard имеет скорость: {self._Gepard__speed} км\ч и {self.LEGS_CNT} лап"


if __name__ == '__main__':
    Gepard1 = FastGepard(90)
    Gepard2 = StrongGepard(100)

    print(Gepard1)
    print(Gepard2)

    print(FastGepard.get_object_count())

    # Используем методы
    print(Gepard1.hunt(10))
    print(Gepard2.rest(5))

# хорошо если
# 1. можем узнать об созданных объектах через метод родителя
# 2. можем узнать через метод наследника о созданных объектах того же класса
# 3. в классах использованы приватные, защищённые атрибуты и использован декоратор @property
# 4. пишем комментарии почему тот или иной метод должен быть в родительском классе или в дочернем
