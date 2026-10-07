# Задание 1
def is_prime():
    try:
        number = int(input("Введите число от 0 до 1000: "))

        if number < 0 or number > 1000:
            raise ValueError("Число должно быть от 0 до 1000.")

        if number < 2:
            print(False)
            return False

        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                print(False)
                return False

        print(True)
        return True

    except ValueError as error:
        print("Ошибка:", error)

    finally:
        print("Проверка на простое число завершена.\n")


# Задание 2
def check_data():
    try:
        print("Выберите тип данных:")
        print("1 - список")
        print("2 - кортеж")
        print("3 - число")
        print("4 - строка")

        choice = input("Ваш выбор: ")

        if choice == "1":
            words = input("Введите слова через пробел: ").split()

            # Проверяем, что получен список
            data = words

            # Считаем длину всех слов
            total_length = sum(len(word) for word in data)

            print("Список:", data)
            print("Суммарная длина всех слов:", total_length)

        elif choice == "2":
            text = input("Введите элементы кортежа через пробел: ")
            data = tuple(text.split())

            letters = 0
            numbers = 0

            for item in data:
                for symbol in item:
                    if symbol.isalpha():
                        letters += 1
                    elif symbol.isdigit():
                        numbers += 1

            print("Кортеж:", data)
            print("Количество букв:", letters)
            print("Количество чисел:", numbers)

        elif choice == "3":
            number = int(input("Введите число: "))

            reversed_number = str(number)[::-1]

            print("Число в обратном порядке:", reversed_number)

        elif choice == "4":
            text = input("Введите строку: ")

            digit_sum = 0

            for symbol in text:
                if symbol.isdigit():
                    digit_sum += int(symbol)

            print("Сумма всех цифр:", digit_sum)

        else:
            raise ValueError("Необходимо выбрать число от 1 до 4.")

    except ValueError as error:
        print("Ошибка:", error)

    finally:
        print("Проверка типа данных завершена.\n")


# Задание 3
def check_matrix():
    try:
        rows = int(input("Введите количество строк матрицы: "))
        columns = int(input("Введите количество столбцов матрицы: "))

        if rows <= 0 or columns <= 0:
            raise ValueError("Размеры матрицы должны быть положительными.")

        if rows != columns:
            print("Матрица не является симметричной.")
            return

        matrix = []

        print("Введите матрицу построчно:")

        for i in range(rows):
            row = list(map(int, input(f"Строка {i + 1}: ").split()))

            if len(row) != columns:
                raise ValueError(
                    f"В строке должно быть {columns} элементов."
                )

            matrix.append(row)

        symmetric = True

        for i in range(rows):
            for j in range(columns):
                if matrix[i][j] != matrix[j][i]:
                    symmetric = False
                    break

        if symmetric:
            print("Матрица является симметричной.")
        else:
            print("Матрица не является симметричной.")

    except ValueError as error:
        print("Ошибка:", error)

    finally:
        print("Проверка матрицы завершена.\n")


# Задание 4
def try_except_finally_demo():
    try:
        print("Демонстрация try / except / finally")

        number = int(input("Введите первое число: "))
        divisor = int(input("Введите второе число: "))

        result = number / divisor

        print("Результат деления:", result)

    except ValueError:
        print("Ошибка: необходимо вводить только числа.")

    except ZeroDivisionError:
        print("Ошибка: на ноль делить нельзя.")

    finally:
        print("Блок finally выполнен.")
        print("Операция завершена.\n")


# Главное меню
while True:
    print("========== МЕНЮ ==========")
    print("1 - Проверить простое число")
    print("2 - Проверить тип данных")
    print("3 - Проверить симметричность матрицы")
    print("4 - Демонстрация try/except/finally")
    print("0 - Выход")
    print("===========================")

    try:
        choice = int(input("Введите номер задания: "))

        if choice == 1:
            is_prime()

        elif choice == 2:
            check_data()

        elif choice == 3:
            check_matrix()

        elif choice == 4:
            try_except_finally_demo()

        elif choice == 0:
            print("Программа завершена.")
            break

        else:
            raise ValueError("Введите число от 0 до 4.")

    except ValueError as error:
        print("Ошибка:", error)