import json


class Book:
    """
        Класс для представления книги в библиотеке.
        Атрибуты:
            id (int): Уникальный идентификатор книги.
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
            status (str): Статус книги ("в наличии" или "выдана").
        """
    def __init__(self, book_id, title, author, year, status="в наличии"):
        """
        Инициализирует объект книги.
        Args:
            book_id (int): Уникальный идентификатор книги.
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
            status (str): Статус книги. По умолчанию "в наличии".
        """
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        """
         Преобразует объект книги в словарь.
         Returns:
             dict: Словарь с данными книги.
         """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        """
        Создает объект книги из словаря.
        Args:
            data (dict): Словарь с данными книги.
        Returns:
            Book: Объект книги.
        """
        return Book(data["id"], data["title"], data["author"], data["year"], data["status"])


class Library:
    """
    Класс для управления библиотекой книг.
    Атрибуты:
        storage_file (str): Имя файла для хранения данных о книгах.
        books (list): Список объектов книг.
    """
    def __init__(self, storage_file="library.json"):
        """
        Инициализирует объект библиотеки и загружает данные из файла.
        Args:
            storage_file (str): Имя файла для хранения данных. По умолчанию "library.json".
        """
        self.storage_file = storage_file
        self.books = []
        self.load_books()

    def load_books(self):
        """
        Загружает книги из файла JSON.

        Если файл не найден, создает пустую библиотеку.
        Если файл поврежден, предлагает восстановить или завершить выполнение программы.
        """
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.books = [Book.from_dict(book) for book in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Ошибка чтения данных. Файл поврежден или пуст.")
            choice = input("Хотите восстановить файл? (да/нет): ").strip().lower()
            if choice == "да":
                self.books = []
            else:
                raise

    def save_books(self):
        """
        Сохраняет данные о книгах в файл JSON.
        """
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):
        """
        Добавляет новую книгу в библиотеку.
        Проверяет корректность ввода данных, уникальность книги и автогенерирует id.
        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (str): Год издания книги.
        """
        if not title.strip():
            print("Ошибка: название книги не может быть пустым.")
            return
        if not author.strip():
            print("Ошибка: автор книги не может быть пустым.")
            return
        try:
            year = int(year)
            if year < 0 or year > 2024:
                print("Ошибка: год должен быть положительным и не превышать текущий.")
                return
        except ValueError:
            print("Ошибка: год должен быть числом.")
            return

        for book in self.books:
            if book.title == title and book.author == author and book.year == year:
                print("Ошибка: такая книга уже существует в библиотеке.")
                return

        new_id = max([book.id for book in self.books], default=0) + 1
        new_book = Book(new_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга добавлена с id {new_id}.")

    def remove_book(self, book_id):
        """
        Удаляет книгу по id.
        Args:
            book_id (str): Идентификатор книги.
        """
        if not self.books:
            print("Библиотека пуста. Удаление невозможно.")
            return
        try:
            book_id = int(book_id)
            if book_id <= 0:
                print("Ошибка: id должен быть положительным числом.")
                return
        except ValueError:
            print("Ошибка: id должен быть числом.")
            return

        book = self.find_book_by_id(book_id)
        if book:
            confirmation = input(f"Вы уверены, что хотите удалить книгу с id {book_id}? (да/нет): ").strip().lower()
            if confirmation != "да":
                print("Удаление отменено.")
                return
            self.books.remove(book)
            self.save_books()
            print(f"Книга с id {book_id} удалена.")
        else:
            print("Книга с таким id не найдена.")

    def find_book_by_id(self, book_id):
        """
        Находит книгу по id.
        Args:
            book_id (int): Идентификатор книги.
        Returns:
            Book: Найденная книга или None.
        """
        return next((book for book in self.books if book.id == book_id), None)

    def search_books(self, key, value):
        """
        Выполняет поиск книг по указанному ключу и значению.
        Args:
            key (str): Поле для поиска (например, "author", "title", "year").
            value (str): Значение для поиска.
        Returns:
            list: Список найденных книг.
        """
        return [book for book in self.books if value.lower() in str(getattr(book, key, "")).lower()]

    def display_books(self):
        """
        Выводит список всех книг в библиотеке.
        """
        if not self.books:
            print("Библиотека пуста.")
        else:
            for book in self.books:
                print(f"{book.id}: {book.title} by {book.author}, {book.year} ({book.status})")

    def change_status(self, book_id, new_status):
        """
        Изменяет статус книги ("в наличии" или "выдана").
        Args:
            book_id (str): Идентификатор книги.
            new_status (str): Новый статус книги.
        """
        if not self.books:
            print("Библиотека пуста. Изменение статуса невозможно.")
            return
        try:
            book_id = int(book_id)
            if book_id <= 0:
                print("Ошибка: id должен быть положительным числом.")
                return
        except ValueError:
            print("Ошибка: id должен быть числом.")
            return

        valid_statuses = ["в наличии", "выдана"]
        if new_status not in valid_statuses:
            print(f"Ошибка: статус должен быть одним из {valid_statuses}.")
            return

        book = self.find_book_by_id(book_id)
        if book:
            book.status = new_status
            self.save_books()
            print(f"Статус книги с id {book_id} изменён на '{new_status}'.")
        else:
            print("Книга с таким id не найдена.")


def main():
    """
    Главная функция программы для управления библиотекой.
    Реализует меню с выбором действий: добавление, удаление, поиск, просмотр всех книг и изменение статуса.
    """
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания книги: ")
            library.add_book(title, author, year)

        elif choice == "2":
            book_id = input("Введите id книги для удаления: ")
            library.remove_book(book_id)

        elif choice == "3":
            if not library.books:
                print("Библиотека пуста. Поиск невозможен.")
                continue
            print("\nМеню поиска:")
            print("1. Поиск по автору")
            print("2. Поиск по названию")
            print("3. Поиск по году")
            search_choice = input("Выберите критерий поиска: ")

            if search_choice == "1":
                author = input("Введите имя автора: ")
                found_books = library.search_books("author", author)
            elif search_choice == "2":
                title = input("Введите название книги: ")
                found_books = library.search_books("title", title)
            elif search_choice == "3":
                year = input("Введите год издания: ")
                found_books = library.search_books("year", year)
            else:
                print("Ошибка: Некорректный выбор.")
                continue

            if found_books:
                for book in found_books:
                    print(f"{book.id}: {book.title} by {book.author}, {book.year} ({book.status})")
            else:
                print("Книги не найдены.")

        elif choice == "4":
            library.display_books()

        elif choice == "5":
            book_id = input("Введите id книги: ")
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            library.change_status(book_id, new_status)

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Ошибка: Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
