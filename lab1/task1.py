import string
from collections import Counter

def task1():
    """
    1. Проверка, является ли последовательность цифр числа 
       справа налево упорядоченной по возрастанию.
    """
    n = input("Введите натуральное число: ").strip()
    if not n.isdigit():
        print("Ошибка: введено не натуральное число.")
        return
    
    # Проверка на то, отсортирована ли она по возрастанию (неубыванию)
    if list(n) == sorted(n):
        print("Да, цифры справа налево упорядочены по возрастанию.")
    else:
        print("Нет, цифры справа налево НЕ упорядочены по возрастанию.")

def task2():
    """
    2. Подсчет гласных и согласных в тексте, вывод согласных при их равенстве 
       и подсчет количества слов.
    """
    text = input("Введите текст: ")
    
    vowels_chars = set("аеёиоуыэюяaeiouyАЕЁИОУЫЭЮЯAEIOUY")
    cons_chars = set("бвгджзйклмнпрстфхцчшщbcdfghjklmnpqrstvwxzБВГДЖЗЙКЛМНПРСТФХЦЧШЩBCDFGHJKLMNPQRSTVWXZ")
    
    vowels = [char for char in text if char in vowels_chars]
    consonants = [char for char in text if char in cons_chars]
    
    count_v = len(vowels)
    count_c = len(consonants)
    
    print(f"Количество гласных: {count_v}")
    print(f"Количество согласных: {count_c}")
    
    if count_v == count_c:
        print("Гласных и согласных поровну! Согласные буквы в тексте:", ", ".join(consonants, ", "))
        
    words = text.split()
    print(f"Количество слов в тексте: {len(words)}")

def task3():
    """
    3. Подсчет количества пар элементов, равных друг другу.
    """
    try:
        lst = list(map(int, input("Введите список чисел через пробел: ").split()))
        counts = Counter(lst)
        # Количество пар для каждого элемента равно n * (n - 1) / 2
        pairs = sum(n * (n - 1) // 2 for n in counts.values())
        print(f"Количество пар одинаковых элементов: {pairs}")
    except ValueError:
        print("Ошибка: необходимо вводить только числа.")

def task4():
    """
    4. Создание словаря из последовательности цифр, где ключ (int) - цифра, 
       значение - ее количество.
    """
    s = input("Введите случайную последовательность чисел от 0 до 9: ").strip()
    result_dict = {}
    
    for char in s:
        if char.isdigit():
            num = int(char)
            result_dict[num] = result_dict.get(num, 0) + 1
            
    print("Результат (Словарь):", result_dict)

def task5():
    """
    5. Программа «Магазин» с 5 пунктами меню.
    """
    # Словарь {Название: [Цена, Количество]}
    shop = {
        "мяч": [150.0, 10],
        "машинка": [300.0, 7],
        "кукла": [500.0, 5],
        "конструктор": [1200.0, 3],
        "пазл": [250.0, 15]
    }
    
    while True:
        print("\n--- МАГАЗИН ИГРУШЕК ---")
        print("1. Просмотр цены")
        print("2. Просмотр количества")
        print("3. Вся информация")
        print("4. Покупка")
        print("5. До свидания")
        
        choice = input("Выберите действие (1-5): ").strip()
        
        if choice == '1':
            print("Цены товаров:")
            for name, data in shop.items():
                print(f"{name.capitalize()} – {data[0]} руб.")
        
        elif choice == '2':
            print("Остаток товаров:")
            for name, data in shop.items():
                print(f"{name.capitalize()} – {data[1]} шт.")
        
        elif choice == '3':
            print("Полная информация о товарах:")
            for name, data in shop.items():
                print(f"Товар: {name.capitalize():<12} | Цена: {data[0]:<7} руб. | Количество: {data[1]} шт.")
        
        elif choice == '4':
            total_price = 0.0
            print("Режим покупки (введите 'n' для завершения покупок и перехода к оплате)")
            while True:
                item = input("Введите название игрушки: ").strip().lower()
                if item == 'n':
                    break
                
                if item not in shop:
                    print("К сожалению, такого товара нет в нашем магазине.")
                    continue
                
                qty_input = input(f"Введите количество товара '{item.capitalize()}': ").strip()
                if not qty_input.isdigit():
                    print("Некорректное количество. Введите целое число.")
                    continue
                
                qty = int(qty_input)
                if qty > shop[item][1]:
                    print(f"Недостаточно товара на складе. Доступно: {shop[item][1]} шт.")
                else:
                    # Уменьшаем количество и считаем цену
                    shop[item][1] -= qty
                    cost = qty * shop[item][0]
                    total_price += cost
                    print(f"В корзину добавлено: {item.capitalize()} ({qty} шт.) на сумму {cost} руб.")
            
            print(f"\n--- ЧЕК ---")
            print(f"Общая сумма к оплате: {total_price} руб.")
            print("Остаток товаров в магазине:")
            for name, data in shop.items():
                print(f"{name.capitalize()} – {data[1]} шт.")
                
        elif choice == '5':
            print("До свидания! Возврат в главное меню.")
            break
        else:
            print("Неверный пункт меню. Попробуйте еще раз.")

def task6():
    """
    6. Вывод кортежа уникальных элементов списка целых чисел в обратном порядке.
    """
    try:
        lst = list(map(int, input("Введите список целых чисел через пробел: ").split()))
        # dict.fromkeys удаляет дубликаты, сохраняя оригинальный порядок. Затем применяем reversed
        unique_reversed_tuple = tuple(reversed(list(dict.fromkeys(lst))))
        print(f"Кортеж уникальных элементов в обратном порядке:\n{unique_reversed_tuple}")
    except ValueError:
        print("Ошибка: необходимо вводить только целые числа.")


def main():
    while True:
        print("\n" + "="*40)
        print("ГЛАВНОЕ МЕНЮ (Задания 1-6)")
        print("="*40)
        print("1. Проверка порядка цифр числа")
        print("2. Анализ текста (гласные/согласные, слова)")
        print("3. Подсчет пар равных элементов списка")
        print("4. Словарь из последовательности цифр")
        print("5. Программа «Магазин»")
        print("6. Кортеж уникальных элементов в обратном порядке")
        print("0. Выход из программы")
        
        action = input("\nВведите номер задания (1-6) или 0 для выхода: ").strip()
        
        if action == '1':
            task1()
        elif action == '2':
            task2()
        elif action == '3':
            task3()
        elif action == '4':
            task4()
        elif action == '5':
            task5()
        elif action == '6':
            task6()
        elif action == '0':
            print("Завершение работы программы.")
            break
        else:
            print("Некорректный ввод! Пожалуйста, выберите число от 0 до 6.")

if __name__ == "__main__":
    main()