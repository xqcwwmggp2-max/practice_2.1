import csv

FILENAME = "practice_2.1/resource/products.csv"
SORTED_FILENAME = "practice_2.1/resource/sorted_products.csv"

def load_products(filename):
    products = []
    with open(filename, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append({
                "Название": row["Название"],
                "Цена": float(row["Цена"]),
                "Количество": int(row["Количество"])
            })
    return products

def save_products(filename, products):
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Название", "Цена", "Количество"])
        writer.writeheader()
        for p in products:
            writer.writerow({
                "Название": p["Название"],
                "Цена": p["Цена"],
                "Количество": p["Количество"]
            })

def add_product(products):
    name = input("Введи название товара: ")
    price = float(input("Введи цену: "))
    quantity = int(input("Введи количество: "))
    products.append({
        "Название": name,
        "Цена": price,
        "Количество": quantity
    })
    print("Я добавил товар.")

def search_product(products):
    name = input("Введи название товара для поиска: ").strip().lower()
    found = False
    for p in products:
        if p["Название"].strip().lower() == name:
            print(f"Найден товар: {p['Название']}, цена: {p['Цена']}, количество: {p['Количество']}")
            found = True
            break
    if not found:
        print("Товар не найден.")

def total_cost(products):
    total = 0
    for p in products:
        total += p["Цена"] * p["Количество"]
    return total

def save_sorted_products(products):
    sorted_products = sorted(products, key=lambda x: x["Цена"])
    save_products(SORTED_FILENAME, sorted_products)

def main():
    products = load_products(FILENAME)

    while True:
        print("\n1. Добавить товар")
        print("2. Поиск товара")
        print("3. Общая стоимость склада")
        print("4. Сохранить и выйти")
        choice = input("Выбери действие: ")

        if choice == "1":
            add_product(products)
        elif choice == "2":
            search_product(products)
        elif choice == "3":
            print("Общая стоимость всех товаров:", total_cost(products))
        elif choice == "4":
            save_products(FILENAME, products)
            save_sorted_products(products)
            print("Я сохранил данные.")
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()