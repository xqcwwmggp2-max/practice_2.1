import json
from pathlib import Path

LIB_FILE = "practice_2.1/resource/library.json"
AVAILABLE_FILE = "practice_2.1/resource/available_books.txt"

def load_books():
    path = Path(LIB_FILE)
    if not path.exists():
        return []
    with open(LIB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_books(books):
    with open(LIB_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

def get_next_id(books):
    if not books:
        return 1
    return max(book["id"] for book in books) + 1

def view_all_books(books):
    if not books:
        print("Список книг пуст.")
        return
    for book in books:
        status = "доступна" if book["available"] else "взята"
        print(f"ID: {book['id']} | {book['title']} | {book['author']} | {book['year']} | {status}")

def search_books(books):
    query = input("Введи автора или название: ").strip().lower()
    found = False
    for book in books:
        if query in book["title"].lower() or query in book["author"].lower():
            status = "доступна" if book["available"] else "взята"
            print(f"ID: {book['id']} | {book['title']} | {book['author']} | {book['year']} | {status}")
            found = True
    if not found:
        print("Книги не найдены.")

def add_book(books):
    title = input("Название: ").strip()
    author = input("Автор: ").strip()
    year = int(input("Год издания: ").strip())
    book = {
        "id": get_next_id(books),
        "title": title,
        "author": author,
        "year": year,
        "available": True
    }
    books.append(book)
    save_books(books)
    print("Книга добавлена.")

def change_status(books):
    book_id = int(input("Введите ID книги: "))
    for book in books:
        if book["id"] == book_id:
            book["available"] = not book["available"]
            save_books(books)
            print("Статус книги изменён.")
            return
    print("Книга с таким ID не найдена.")

def delete_book(books):
    book_id = int(input("Введи ID книги для удаления: "))
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            save_books(books)
            print("Книга удалена.")
            return
    print("Книга с таким ID не найдена.")

def export_available_books(books):
    available = [book for book in books if book["available"]]
    with open(AVAILABLE_FILE, "w", encoding="utf-8") as f:
        if not available:
            f.write("Нет доступных книг.\n")
        else:
            for book in available:
                f.write(f"{book['id']}. {book['title']} — {book['author']} ({book['year']})\n")
    print("Доступные книги экспортированы в available_books.txt")

def main():
    books = load_books()

    while True:
        print("\n1. Просмотр всех книг")
        print("2. Поиск по автору/названию")
        print("3. Добавить новую книгу")
        print("4. Изменить статус доступности")
        print("5. Удалить книгу по ID")
        print("6. Экспорт доступных книг")
        print("7. Выход")

        choice = input("Выбери действие: ").strip()

        if choice == "1":
            view_all_books(books)
        elif choice == "2":
            search_books(books)
        elif choice == "3":
            add_book(books)
        elif choice == "4":
            change_status(books)
        elif choice == "5":
            delete_book(books)
        elif choice == "6":
            export_available_books(books)
        elif choice == "7":
            print("Выход.")
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()