from data_service import load_books, save_books, DEFAULT_PATH


def _next_id(books):
    if not books:
        return 1
    return max(b["id"] for b in books) + 1


def add_book(title, author, year, status="unread", path=DEFAULT_PATH):
    """Добавляет книгу. Валидирует title (непустой) и year (положительное число)."""
    if not title or not title.strip():
        raise ValueError("Название книги не может быть пустым")
    if not isinstance(year, int) or year <= 0:
        raise ValueError("Год должен быть положительным числом")

    books = load_books(path)
    new_book = {
        "id": _next_id(books),
        "title": title.strip(),
        "author": author.strip(),
        "year": year,
        "status": status,
    }
    books.append(new_book)
    save_books(books, path)
    return new_book


def get_all_books(path=DEFAULT_PATH):
    return load_books(path)


def _find_book_index(books, book_id):
    for i, b in enumerate(books):
        if b["id"] == book_id:
            return i
    raise KeyError(f"Книга с id={book_id} не найдена")


def update_book(book_id, title=None, author=None, year=None, status=None, path=DEFAULT_PATH):
    books = load_books(path)
    idx = _find_book_index(books, book_id)

    if title is not None:
        books[idx]["title"] = title
    if author is not None:
        books[idx]["author"] = author
    if year is not None:
        books[idx]["year"] = year
    if status is not None:
        books[idx]["status"] = status

    save_books(books, path)
    return books[idx]


def delete_book(book_id, path=DEFAULT_PATH):
    books = load_books(path)
    idx = _find_book_index(books, book_id)
    removed = books.pop(idx)
    save_books(books, path)
    return removed


def mark_as_read(book_id, path=DEFAULT_PATH):
    return update_book(book_id, status="read", path=path)


def search_books(query, path=DEFAULT_PATH):
    """Ищет по названию или автору, без учёта регистра. Пустой запрос -> все книги."""
    books = load_books(path)
    if not query.strip():
        return books

    query_lower = query.strip().lower()
    return [
        b for b in books
        if query_lower in b["title"].lower() or query_lower in b["author"].lower()
    ]


def filter_by_status(status, path=DEFAULT_PATH):
    books = load_books(path)
    return [b for b in books if b["status"] == status]
