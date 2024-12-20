def calc(a, b, op):
    try:
        int(a)
        int(b)
    except ValueError:
        print("Введенные данные не являются числом")
    else:
        a1 = int(a)
        b1 = int(b)
        match op:
            case "+":
                return a1 + b1
            case "-":
                return a1 - b1
            case "*":
                return a1 * b1
            case "/":
                if (b1 == 0):
                    return "ВВЕДЕНО НЕКОРЕКТНОЕ ЧИСЛО"
                else:
                    return a1 / b1
            case _:
                print("Введен некоректный оператор")

# тут проверить работу функции

print(calc('135', 0, '/'))
