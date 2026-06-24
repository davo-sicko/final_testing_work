import os
import pytest
from data_service import load_books, save_books

TEST_FILE = "data/test_books.csv"


@pytest.fixture(autouse=True)
def cleanup():
    """Удаляем тестовый файл до и после каждого теста, чтобы тесты не влияли друг на друга."""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def test_load_books_no_file_returns_empty_list():
    """Если файла нет — возвращаем пустой список, а не падаем с ошибкой."""
    result = load_books(TEST_FILE)
    assert result == []


def test_save_and_load_one_book():
    books = [{"id": 1, "title": "1984", "author": "Оруэлл", "year": 1949, "status": "unread"}]
    save_books(books, TEST_FILE)
    loaded = load_books(TEST_FILE)
    assert loaded == books


def test_save_and_load_multiple_books():
    books = [
        {"id": 1, "title": "1984", "author": "Оруэлл", "year": 1949, "status": "unread"},
        {"id": 2, "title": "Дюна", "author": "Герберт", "year": 1965, "status": "read"},
    ]
    save_books(books, TEST_FILE)
    loaded = load_books(TEST_FILE)
    assert loaded == books


def test_load_books_year_and_id_are_int_not_str():
    """Краевой случай: CSV хранит всё как текст, но year и id должны вернуться как int."""
    books = [{"id": 1, "title": "Test", "author": "A", "year": 2000, "status": "unread"}]
    save_books(books, TEST_FILE)
    loaded = load_books(TEST_FILE)
    assert isinstance(loaded[0]["id"], int)
    assert isinstance(loaded[0]["year"], int)


def test_save_books_overwrites_file():
    save_books([{"id": 1, "title": "A", "author": "B", "year": 2000, "status": "unread"}], TEST_FILE)
    save_books([{"id": 2, "title": "C", "author": "D", "year": 2010, "status": "read"}], TEST_FILE)
    loaded = load_books(TEST_FILE)
    assert len(loaded) == 1
    assert loaded[0]["id"] == 2
