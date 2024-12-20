"""Практическая работа №6."""

# Вводная часть
# -------------

"""
Многие системы нуждаются в разграничении прав пользователей.
"""

# Задание
# ----------

"""
Нужно написать "сценарий" такой системы. И подкрепить её прототипом такой системы.

У нас есть несколько функций, которые реализуют функционал системы, но к каждой функции доступ имеют не все пользователи.

Эти функции следует декорировать так, чтобы текущий пользователь системы понимал, имеет ли он к ней доступ при обращении к этой функции.

Представим, что система создаётся для некой области применения.
Варианты зависян он номера в списке (остаток от деления на 10).
0 — база данных
1 — API системы
2 — система документооборота
3 — склад
4 — супермаркет
5 — университет
6 — поликлиника
7 — военный объект
8 — центр управления полётами
9 — химическая/биологическая лаборатория

В системе должны быть представлены следующие роли:
1. Полные права (администратор /генерал /главврач /ректор…)
2. Ограниченные стандартные права (сотрудники)
3. Гостевые права (не залогиненный пользователь)
Следует предусмотреть:
4. Персональные права


В прототипе системы должны быть учтены следующие функции:
- работа с пользователями (добавление, удаление, редактирование)
- доступ к какому-то объекту с ограниченным доступом
- доступ к какому-то объекту с публичным доступом
- система доступа должна быть дружелюбной
- есть возможность изменить права какого-то пользователя

"""

# Шаблон-пример
# ----------

users = {
    'admin': {'role': 'admin', 'permissions': ['user_management', 'restricted_access', 'public_access']},
    'employee1': {'role': 'employee', 'permissions': ['restricted_access', 'public_access']},
    'guest': {'role': 'guest', 'permissions': ['public_access']},
    'john_doe': {'role': 'custom', 'permissions': ['public_access']} #персональные права
}

current_user = 'guest'

def user_level(required_permissions):
    """
    Декоратор для проверки уровня доступа пользователя.

    Args:
        required_permissions (list): Список требуемых прав доступа.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):

            if current_user not in users:
                print(f"Пользователь '{current_user}' не найден")
                return
            user_permissions = users[current_user]['permissions']

            if any(perm in user_permissions for perm in required_permissions):
                print(f"Пользователь '{current_user}' имеет право доступа к '{func.__name__}'")
                return func(*args, **kwargs)
            else:
                print(f"У пользователя '{current_user}' нет прав доступа к '{func.__name__}'")
        return wrapper
    return decorator

@user_level(['user_management'])
def create_user(user):
    """
    Создает нового пользователя.

    Args:
        user (dict): Словарь с данными пользователя.
    """
    print(f"Создание пользователя: {user}")
    users[user['username']] = {'role':user['role'], 'permissions':user['permissions']}

@user_level(['user_management'])
def delete_user(user):
    """
    Удаляет пользователя.

    Args:
        user (str): Имя пользователя, которого нужно удалить.
    """
    if user in users:
      del users[user]
      print(f"Пользователь {user} удален.")
    else:
      print(f"Пользователь {user} не найден")

@user_level(['user_management'])
def edit_user(user, new_permissions):
    """
    Изменяет права пользователя.

    Args:
        user (str): Имя пользователя, чьи права нужно изменить.
        new_permissions (list): Новый список прав доступа.
    """
    if user in users:
        users[user]['permissions'] = new_permissions
        print(f"Права пользователя '{user}' обновлены: {new_permissions}")
    else:
      print(f"Пользователь {user} не найден")


@user_level(['restricted_access'])
def restricted_resource():
    """
    Функция для доступа к ресурсу с ограниченным доступом.
    """
    print("Доступ к ресурсу с ограниченным доступом")

@user_level(['public_access'])
def public_resource():
    """
    Функция для доступа к публичному ресурсу.
    """
    print("Доступ к публичному ресурсу")

def change_current_user(user):
    """
    Изменяет текущего пользователя в системе.

    Args:
        user (str): Имя пользователя, на которого нужно переключиться.
    """
    global current_user
    if user in users:
      current_user = user
      print(f"Текущий пользователь изменен на: '{user}'")
    else:
       print(f"Пользователь '{user}' не найден")


# Сценарии
# ---------------
"""
Например,

- администратор изменил права рользователю, он зашёл в систему и смог сделать, то что не мог до этого
- зашёл гость, но не смог запустить ракету
- придумайте сами в зависимости от области в которой "проектируется" система доступа
"""


# Самопроверка
# ---------------

# 1. есть декоратор с параметром.
# 2. есть сценарий, который позволяет продемонстрировать последовательность действий.

# Сценарий 1: Администратор меняет права пользователя и пользователь получает доступ

print("\n---- Сценарий 1: Администратор меняет права пользователя ----\n")

change_current_user('admin')

print("\n- Создание пользователя John Doe\n")
create_user({'username':'john_doe', 'role':'custom', 'permissions':['public_access']})

print("\n- Попытка доступа к ресурсу с ограниченным доступом пользователем John Doe с публичным доступом\n")
change_current_user('john_doe')
restricted_resource()


print("\n- Администратор изменяет права John Doe для доступа к ограниченному ресурсу\n")
change_current_user('admin')
edit_user('john_doe', ['restricted_access', 'public_access'])


print("\n- Попытка доступа к ресурсу с ограниченным доступом пользователем John Doe\n")
change_current_user('john_doe')
restricted_resource()

# Сценарий 2: Гость не может получить доступ к ограниченным ресурсам

print("\n---- Сценарий 2: Попытка доступа гостя ----\n")

change_current_user('guest')

print("\n- Попытка доступа к ресурсу с ограниченным доступом гостем\n")

restricted_resource()

print("\n- Гость имеет доступ к публичному ресурсу\n")
public_resource()

#Сценарий 3: Удаление пользователя

print("\n---- Сценарий 3: Администратор удаляет пользователя ----\n")

change_current_user('admin')

print("\n- Попытка удалить пользователя employee1\n")
delete_user('employee1')

print("\n- Попытка доступа к ресурсу под удаленным пользователем\n")
change_current_user('employee1')
restricted_resource()

print("\n- Попытка повторно удалить удалённого пользователя\n")
change_current_user('admin')
delete_user('employee1')