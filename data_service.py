import csv
import os

FIELDNAMES = ["id", "title", "author", "year", "status"]
DEFAULT_PATH = "data/books.csv"


def load_books(path=DEFAULT_PATH):
    """Читает книги из CSV. Если файла нет — возвращает пустой список."""
    if not os.path.exists(path):
        return []

    books = []
    with open(path, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append({
                "id": int(row["id"]),
                "title": row["title"],
                "author": row["author"],
                "year": int(row["year"]),
                "status": row["status"],
            })
    return books


def save_books(books, path=DEFAULT_PATH):
    """Полностью перезаписывает CSV списком книг."""
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    with open(path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for book in books:
            writer.writerow(book)
