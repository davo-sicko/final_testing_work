"""
Тесты-репродюсеры для дефектов, найденных в ходе имитации поддержки (Этап 5).
Каждый тест соответствует конкретному Issue и должен падать ДО фикса
и проходить ПОСЛЕ.
"""
import os
import pytest
import logic

TEST_FILE = "data/test_support_books.csv"


@pytest.fixture(autouse=True)
def cleanup():
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


# --- BUG-001: пустой автор принимается без ошибки ---

def test_bug001_add_book_empty_author_raises_error():
    """
    Issue BUG-001.
    До фикса: add_book("Title", "", 2020) не выбрасывал ошибку,
    книга сохранялась с пустым полем author.
    После фикса: пустой/пробельный author должен отклоняться так же,
    как и пустой title.
    """
    with pytest.raises(ValueError):
        logic.add_book("Title", "", 2020, path=TEST_FILE)


def test_bug001_add_book_whitespace_author_raises_error():
    with pytest.raises(ValueError):
        logic.add_book("Title", "   ", 2020, path=TEST_FILE)


def test_bug001_add_book_valid_author_still_works():
    """Регрессия: валидный автор не должен сломаться после фикса."""
    book = logic.add_book("Title", "Нормальный Автор", 2020, path=TEST_FILE)
    assert book["author"] == "Нормальный Автор"


# --- BUG-002: update_book принимает произвольное значение status ---

def test_bug002_update_book_invalid_status_raises_error():
    """
    Issue BUG-002.
    До фикса: update_book(id, status="anything") принимал любую строку,
    и книга пропадала из обоих фильтров (read/unread).
    После фикса: допускаются только "read" и "unread".
    """
    book = logic.add_book("Title", "Author", 2020, path=TEST_FILE)
    with pytest.raises(ValueError):
        logic.update_book(book["id"], status="something_invalid", path=TEST_FILE)


def test_bug002_update_book_valid_statuses_still_work():
    """Регрессия: допустимые статусы продолжают работать."""
    book = logic.add_book("Title", "Author", 2020, path=TEST_FILE)
    updated_read = logic.update_book(book["id"], status="read", path=TEST_FILE)
    assert updated_read["status"] == "read"
    updated_unread = logic.update_book(book["id"], status="unread", path=TEST_FILE)
    assert updated_unread["status"] == "unread"


def test_bug002_book_after_invalid_status_attempt_is_findable_in_filters():
    """
    После отклонения некорректного статуса книга обязана остаться
    видимой хотя бы в одном из фильтров (не "потеряться").
    """
    book = logic.add_book("Title", "Author", 2020, path=TEST_FILE)
    try:
        logic.update_book(book["id"], status="bad_value", path=TEST_FILE)
    except ValueError:
        pass
    all_books = logic.filter_by_status("read", path=TEST_FILE) + logic.filter_by_status("unread", path=TEST_FILE)
    assert len(all_books) == 1
