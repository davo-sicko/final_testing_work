import os
import pytest
import logic

TEST_FILE = "data/test_logic_books.csv"


@pytest.fixture(autouse=True)
def cleanup():
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


# --- add_book ---

def test_add_book_assigns_incremental_id():
    b1 = logic.add_book("1984", "Оруэлл", 1949, path=TEST_FILE)
    b2 = logic.add_book("Дюна", "Герберт", 1965, path=TEST_FILE)
    assert b1["id"] == 1
    assert b2["id"] == 2


def test_add_book_default_status_is_unread():
    book = logic.add_book("1984", "Оруэлл", 1949, path=TEST_FILE)
    assert book["status"] == "unread"


def test_add_book_empty_title_raises_error():
    """Краевой случай: пустое название недопустимо."""
    with pytest.raises(ValueError):
        logic.add_book("", "Оруэлл", 1949, path=TEST_FILE)


def test_add_book_invalid_year_raises_error():
    """Краевой случай: год должен быть положительным числом."""
    with pytest.raises(ValueError):
        logic.add_book("1984", "Оруэлл", -5, path=TEST_FILE)


# --- get_all_books / list ---

def test_get_all_books_empty_when_no_books():
    assert logic.get_all_books(path=TEST_FILE) == []


def test_get_all_books_returns_added_books():
    logic.add_book("1984", "Оруэлл", 1949, path=TEST_FILE)
    books = logic.get_all_books(path=TEST_FILE)
    assert len(books) == 1
    assert books[0]["title"] == "1984"


# --- update_book ---

def test_update_book_changes_fields():
    book = logic.add_book("1984", "Оруэлл", 1949, path=TEST_FILE)
    updated = logic.update_book(book["id"], title="1984 (испр.)", path=TEST_FILE)
    assert updated["title"] == "1984 (испр.)"
    assert updated["author"] == "Оруэлл"  # остальное не меняется


def test_update_book_nonexistent_id_raises_error():
    """Краевой случай: обновление отсутствующей книги."""
    with pytest.raises(KeyError):
        logic.update_book(999, title="X", path=TEST_FILE)


# --- delete_book ---

def test_delete_book_removes_it():
    book = logic.add_book("1984", "Оруэлл", 1949, path=TEST_FILE)
    logic.delete_book(book["id"], path=TEST_FILE)
    assert logic.get_all_books(path=TEST_FILE) == []


def test_delete_book_nonexistent_id_raises_error():
    with pytest.raises(KeyError):
        logic.delete_book(999, path=TEST_FILE)


# --- mark_as_read ---

def test_mark_as_read_changes_status():
    book = logic.add_book("1984", "Оруэлл", 1949, path=TEST_FILE)
    updated = logic.mark_as_read(book["id"], path=TEST_FILE)
    assert updated["status"] == "read"


# --- search ---

def test_search_by_title_case_insensitive():
    logic.add_book("1984", "Оруэлл", 1949, path=TEST_FILE)
    logic.add_book("Дюна", "Герберт", 1965, path=TEST_FILE)
    result = logic.search_books("дюна", path=TEST_FILE)
    assert len(result) == 1
    assert result[0]["title"] == "Дюна"


def test_search_by_author():
    logic.add_book("1984", "Оруэлл", 1949, path=TEST_FILE)
    result = logic.search_books("оруэлл", path=TEST_FILE)
    assert len(result) == 1


def test_search_no_match_returns_empty_list():
    logic.add_book("1984", "Оруэлл", 1949, path=TEST_FILE)
    result = logic.search_books("несуществующая книга", path=TEST_FILE)
    assert result == []


def test_search_empty_query_returns_all_books():
    """Краевой случай: пустой запрос — не ошибка, а просто весь список."""
    logic.add_book("1984", "Оруэлл", 1949, path=TEST_FILE)
    result = logic.search_books("", path=TEST_FILE)
    assert len(result) == 1


# --- filter by status ---

def test_filter_by_status_read():
    b1 = logic.add_book("1984", "Оруэлл", 1949, path=TEST_FILE)
    logic.add_book("Дюна", "Герберт", 1965, path=TEST_FILE)
    logic.mark_as_read(b1["id"], path=TEST_FILE)
    result = logic.filter_by_status("read", path=TEST_FILE)
    assert len(result) == 1
    assert result[0]["title"] == "1984"


# --- IMPROVEMENT-001: сортировка по году издания ---

def test_get_all_books_sorted_by_year():
    logic.add_book("Дюна", "Герберт", 1965, path=TEST_FILE)
    logic.add_book("1984", "Оруэлл", 1949, path=TEST_FILE)
    logic.add_book("Сияние", "Кинг", 1977, path=TEST_FILE)
    sorted_books = logic.get_all_books_sorted_by_year(path=TEST_FILE)
    years = [b["year"] for b in sorted_books]
    assert years == [1949, 1965, 1977]


def test_get_all_books_sorted_by_year_empty_list():
    assert logic.get_all_books_sorted_by_year(path=TEST_FILE) == []
