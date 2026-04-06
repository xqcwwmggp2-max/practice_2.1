import math
from datetime import datetime
from pathlib import Path

log_file = "practice_2.1/resource/calculator.log"

def write_log(text):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}\n")

def show_last_operations():
    path = Path(log_file)
    if not path.exists():
        print("Лог-файл еще не создан.")
        return

    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print("\nПоследние 5 операций:")
    if not lines:
        print("Лог-файл пустой.")
        return

    for line in lines[-5:]:
        print(line.rstrip())

def clear_log():
    with open(log_file, "w", encoding="utf-8") as f:
        pass
    print("Лог-файл очищен.")

def calculator():
    show_last_operations()

    while True:
        print("\nВыбери действие:")
        print("1. Посчитать")
        print("2. Очистить лог-файл")
        print("3. Выход")
        choice = input("Твой выбор: ").strip()

        if choice == "1":
            op = input("Введи операцию (+, -, *, /, log, sin): ").strip()

            try:
                a = float(input("Введи первое число: "))

                if op in ["+", "-", "*", "/"]:
                    b = float(input("Введи второе число: "))

                    if op == "+":
                        result = a + b
                    elif op == "-":
                        result = a - b
                    elif op == "*":
                        result = a * b
                    elif op == "/":
                        if b == 0:
                            print("Нельзя делить на ноль...")
                            continue
                        result = a / b

                    text = f"{a:g} {op} {b:g} = {result:g}"
                    print("Результат:", result)
                    write_log(text)

                elif op == "log":
                    if a <= 0:
                        print("Логарифм можно вычислить только для числа > 0.")
                        continue
                    result = math.log(a)
                    text = f"log({a:g}) = {result:g}"
                    print("Результат:", result)
                    write_log(text)

                elif op == "sin":
                    result = math.sin(a)
                    text = f"sin({a:g}) = {result:g}"
                    print("Результат:", result)
                    write_log(text)

                else:
                    print("Я не знаю такую операцию.")

            except ValueError:
                print("Ошибка: введи корректные числа.")

        elif choice == "2":
            clear_log()

        elif choice == "3":
            print("Программа завершена.")
            break

        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    calculator()