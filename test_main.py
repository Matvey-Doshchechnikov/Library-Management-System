import unittest
from main import Book, Library


class TestLibrary(unittest.TestCase):

    def setUp(self):
        """
        Этот метод вызывается перед каждым тестом.
        Создаем объект библиотеки с временным хранилищем.
        """
        self.library = Library("test_library.json")
        self.library.books = []  # очищаем библиотеку перед каждым тестом

    def test_add_book(self):
        """Тест добавления книги в библиотеку."""
        self.library.add_book("Book Title", "Author Name", "2020")
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Book Title")
        self.assertEqual(self.library.books[0].author, "Author Name")
        self.assertEqual(self.library.books[0].year, 2020)
        self.assertEqual(self.library.books[0].status, "в наличии")

    def test_remove_book(self):
        """Тест удаления книги из библиотеки по id."""
        self.library.add_book("Book Title", "Author Name", "2020")
        book_id = self.library.books[0].id
        self.library.remove_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_remove_non_existent_book(self):
        """Тест попытки удалить несуществующую книгу."""
        self.library.add_book("Book Title", "Author Name", "2020")
        self.library.remove_book(9999)  # неверный ID
        self.assertEqual(len(self.library.books), 1)  # Книга не должна быть удалена

    def test_change_status(self):
        """Тест изменения статуса книги."""
        self.library.add_book("Book Title", "Author Name", "2020")
        book_id = self.library.books[0].id
        self.library.change_status(book_id, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

    def test_search_books_by_author(self):
        """Тест поиска книги по автору."""
        self.library.add_book("Book Title", "Author Name", "2020")
        found_books = self.library.search_books("author", "Author Name")
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].author, "Author Name")

    def test_search_books_by_title(self):
        """Тест поиска книги по названию."""
        self.library.add_book("Book Title", "Author Name", "2020")
        found_books = self.library.search_books("title", "Book Title")
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].title, "Book Title")

    def test_search_books_by_year(self):
        """Тест поиска книги по году."""
        self.library.add_book("Book Title", "Author Name", "2020")
        found_books = self.library.search_books("year", "2020")
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].year, 2020)

    def test_invalid_status_change(self):
        """Тест попытки изменить статус на некорректное значение."""
        self.library.add_book("Book Title", "Author Name", "2020")
        book_id = self.library.books[0].id
        self.library.change_status(book_id, "invalid_status")
        self.assertEqual(self.library.books[0].status, "в наличии")  # Статус не должен измениться

    def test_empty_library(self):
        """Тест пустой библиотеки."""
        self.assertEqual(len(self.library.books), 0)
        self.library.display_books()  # Проверяем, что выводится сообщение "Библиотека пуста."

    def test_invalid_year_in_add_book(self):
        """Тест добавления книги с некорректным годом."""
        self.library.add_book("Book Title", "Author Name", "invalid_year")
        self.assertEqual(len(self.library.books), 0)  # Книга не должна быть добавлена

    def test_duplicate_book(self):
        """Тест добавления одинаковых книг."""
        self.library.add_book("Book Title", "Author Name", "2020")
        self.library.add_book("Book Title", "Author Name", "2020")
        self.assertEqual(len(self.library.books), 1)  # Книга не должна быть добавлена повторно


if __name__ == "__main__":
    unittest.main()
