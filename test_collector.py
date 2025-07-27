from main import BooksCollector
import pytest



class TestBooksCollector:


    @pytest.mark.parametrize(
        "book_name, expected_result",
        [
            ("Сильмариллион", True),
            ("", False),
            ("A" * 41, False),
            ("A" * 40, True),
            ("A" * 1, True),
        ]
    )
    def test_add_new_book(self, book_name, expected_result):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert (book_name in collector.get_books_genre()) == expected_result


    @pytest.mark.parametrize(
        "book_name, genre, expected_genre",
        [
            ("Сильмариллион", "Фантастика", "Фантастика"),
            ("Сильмариллион", "Отсутствует", ""),
        ]
    )
    def test_set_book_genre(self, book_name, genre, expected_genre):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == expected_genre

    def test_set_book_genre_nonexistent_book(self):
        collector = BooksCollector()
        collector.set_book_genre("Отсутствующая книга", "Фантастика")
        assert "Отсутствующая книга" not in collector.get_books_genre()


    @pytest.mark.parametrize(
        "book_name, genre, expected_result",
        [
            ("Сильмариллион", "Фантастика", "Фантастика"),
            ("Отсутствующая книга", None, None),
        ]
    )
    def test_get_book_genre(self, book_name, genre, expected_result):
        collector = BooksCollector()
        if genre is not None:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == expected_result

    
    @pytest.mark.parametrize(
        "books, genre, expected_books",
        [
            (
                [("Сильмариллион", "Фантастика"), ("Властелин Колец", "Фантастика")],
                "Фантастика",
                ["Сильмариллион", "Властелин Колец"]
            ),
            (
                [("Сильмариллион", "Фантастика")],
                "Несуществующий",
                []
            ),
        ]
    )
    def test_get_books_with_specific_genre(self, books, genre, expected_books):
        collector = BooksCollector()
        for book_name, book_genre in books:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, book_genre)
        assert collector.get_books_with_specific_genre(genre) == expected_books

    def test_get_books_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Звездные войны")
        collector.set_book_genre("Звездные войны", "Фантастика")
        assert isinstance(collector.get_books_genre(), dict)
        assert collector.get_books_genre() == {"Звездные войны": "Фантастика"}


    @pytest.mark.parametrize(
        "books, expected_children_books",
        [
            (
                [("Звездные войны", "Фантастика"), ("Поворот не туда", "Ужасы")],
                ["Звездные войны"]
            ),
            (
                [("Мультфильм", "Мультфильмы"), ("Детектив", "Детективы")],
                ["Мультфильм"]
            ),
        ]
    )
    def test_get_books_for_children(self, books, expected_children_books):
        collector = BooksCollector()
        for book_name, genre in books:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, genre)
        assert collector.get_books_for_children() == expected_children_books


    @pytest.mark.parametrize(
        "book_name, expected_result",
        [
            ("Сильмариллион", True),
            ("Несуществующая книга", False),
        ]
    )
    def test_add_book_in_favorites(self, book_name, expected_result):
        collector = BooksCollector()
        if expected_result:
            collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert (book_name in collector.get_list_of_favorites_books()) == expected_result

    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        book_name = "Сильмариллион"
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        assert book_name not in collector.get_list_of_favorites_books()

    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        books = ["Сильмариллион", "Властелин Колец"]
        for book in books:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)
        assert collector.get_list_of_favorites_books() == books