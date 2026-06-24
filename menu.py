import logic


def print_book(book):
    status_label = "✅ прочитано" if book["status"] == "read" else "📖 не прочитано"
    print(f"[{book['id']}] {book['title']} — {book['author']} ({book['year']}) — {status_label}")


def show_menu():
    print("\n=== Личная библиотека ===")
    print("1. Показать все книги")
    print("2. Добавить книгу")
    print("3. Найти книгу")
    print("4. Отметить как прочитанную")
    print("5. Редактировать книгу")
    print("6. Удалить книгу")
    print("7. Фильтр по статусу")
    print("0. Выход")


def handle_list():
    books = logic.get_all_books()
    if not books:
        print("Список пуст.")
        return
    for b in books:
        print_book(b)


def handle_add():
    title = input("Название: ").strip()
    author = input("Автор: ").strip()
    try:
        year = int(input("Год издания: ").strip())
    except ValueError:
        print("Ошибка: год должен быть числом.")
        return

    try:
        book = logic.add_book(title, author, year)
        print(f"Добавлено: {book['title']} (id={book['id']})")
    except ValueError as e:
        print(f"Ошибка: {e}")


def handle_search():
    query = input("Введите название или автора: ").strip()
    results = logic.search_books(query)
    if not results:
        print("Ничего не найдено.")
        return
    for b in results:
        print_book(b)


def handle_mark_read():
    try:
        book_id = int(input("ID книги: ").strip())
        book = logic.mark_as_read(book_id)
        print(f"«{book['title']}» отмечена прочитанной.")
    except ValueError:
        print("Ошибка: ID должен быть числом.")
    except KeyError as e:
        print(f"Ошибка: {e}")


def handle_update():
    try:
        book_id = int(input("ID книги: ").strip())
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return

    print("Оставьте поле пустым, если не нужно менять.")
    title = input("Новое название: ").strip() or None
    author = input("Новый автор: ").strip() or None
    year_input = input("Новый год: ").strip()
    year = int(year_input) if year_input else None

    try:
        book = logic.update_book(book_id, title=title, author=author, year=year)
        print(f"Обновлено: {book['title']}")
    except KeyError as e:
        print(f"Ошибка: {e}")


def handle_delete():
    try:
        book_id = int(input("ID книги: ").strip())
        removed = logic.delete_book(book_id)
        print(f"Удалено: {removed['title']}")
    except ValueError:
        print("Ошибка: ID должен быть числом.")
    except KeyError as e:
        print(f"Ошибка: {e}")


def handle_filter():
    status = input("Статус (read/unread): ").strip()
    results = logic.filter_by_status(status)
    if not results:
        print("Нет книг с таким статусом.")
        return
    for b in results:
        print_book(b)


ACTIONS = {
    "1": handle_list,
    "2": handle_add,
    "3": handle_search,
    "4": handle_mark_read,
    "5": handle_update,
    "6": handle_delete,
    "7": handle_filter,
}


def main():
    while True:
        show_menu()
        choice = input("Выберите пункт: ").strip()
        if choice == "0":
            print("До встречи!")
            break
        action = ACTIONS.get(choice)
        if action:
            action()
        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()
