from database.shared import db
import mysql.connector


class Book:
    def __init__(self, id: int, isbn_book: str, title_book: str, limit_days_loan: int, year_book: int, synopsis_book: str,
                 id_publisher: int, name_publisher: str = None, name_author: str = None, name_category: str = None,
                 id_copy: int = None, available_copy: bool = None) -> None:
        self.id = id
        self.isbn_book = isbn_book
        self.title_book = title_book
        self.limit_days_loan = limit_days_loan
        self.year_book = year_book
        self.synopsis_book = synopsis_book
        self.id_publisher = id_publisher
        self.name_publisher = name_publisher,
        self.name_author = name_author,
        self.name_category = name_category
        self.id_copy = id_copy
        self.available_copy = available_copy

    # Adicionar livros
    @classmethod
    def new(cls, isbn_book, title_book, limit_days_loan, year_book, synopsis_book, id_publisher):
        new_book = '''
            INSERT INTO 
            tb_book(isbn_book, title_book, limit_days_loan, year_book, synopsis_book, id_publisher)
            VALUES
                (%s, %s, %s, %s, %s, %s);
        '''
        try:
            parameters = [isbn_book, title_book, limit_days_loan,
                          year_book, synopsis_book, id_publisher]
            id = db.execute(new_book, parameters, commit=True)
            return Book(id, isbn_book, title_book, limit_days_loan, year_book, synopsis_book, id_publisher)
        except mysql.connector.Error as err:
            return err.errno

    # Consultar todos os livros
    @classmethod
    def list_book(cls):
        list_book = db.execute('SELECT * FROM vw_book;')
        books = []
        for book in list_book:
            books.append(Book(
                book.id_book,
                book.isbn_book,
                book.title_book,
                book.limit_days_loan,
                book.year_book,
                book.synopsis_book or "",
                book.id_publisher,
                book.name_publisher,
                book.name_author,
                book.name_category,
                book.id_copy,
                book.available_copy
            ))
        return books

    # Consultar livros específicos
    @classmethod
    def find_book_by_data(cls, book_parameter):
        list_book = db.execute(
            '''SELECT * FROM vw_book
            WHERE isbn_book = %s
            OR title_book LIKE %s
            OR year_book = %s
            LIMIT 10;''',
            [
                book_parameter,
                ("%" + book_parameter + "%"),
                book_parameter
            ]
        )
        books = []
        for book in list_book:
            books.append(Book(
                book.id_book,
                book.isbn_book,
                book.title_book,
                book.limit_days_loan,
                book.year_book,
                book.synopsis_book or "",
                book.id_publisher,
                book.name_publisher,
                book.name_author,
                book.name_category,
                book.id_copy,
                book.available_copy
            ))
        return books

    @classmethod
    def find_book_by_isbn(cls, isbn: str):
        specific_book = db.execute(
            '''
            SELECT * FROM vw_book
                WHERE isbn_book = %s
            LIMIT 1;
            ''',
            [isbn]
        )[0]
        return Book(
            specific_book.id_book,
            specific_book.isbn_book,
            specific_book.title_book,
            specific_book.limit_days_loan,
            specific_book.year_book,
            specific_book.synopsis_book or "",
            specific_book.id_publisher,
            specific_book.name_publisher,
            specific_book.name_author,
            specific_book.name_category,
            available_copy=specific_book.available_copy
        )

    @classmethod
    def find_available_books_by_isbn(cls, isbn):
        list_book = db.execute(
            '''
            SELECT * FROM vw_book
                WHERE isbn_book = %s
                    AND available_copy = 1;
            ''',
            [isbn]
        )[0]
        books = []
        for book in list_book:
            books.append(Book(
                book.id_book,
                book.isbn_book,
                book.title_book,
                book.limit_days_loan,
                book.year_book,
                book.synopsis_book or "",
                book.id_publisher,
                book.name_publisher,
                book.name_author,
                book.name_category,
                book.id_copy,
                book.available_copy
            ))
        return books

    # Alterar livros específicos
    @classmethod
    def edit_book(cls, isbn_book, title_book, limit_days_loan, year_book, synopsis_book, id_publisher):
        book = Book.find_book_by_isbn(isbn_book)
        db.execute(
            '''UPDATE tb_book SET
            title_book = %s,
            limit_days_loan = %s,
            year_book = %s,
            synopsis_book = %s,
            id_publisher = %s
            WHERE isbn_book = %s
            LIMIT 1;''',
            [
                title_book or book.title_book,
                limit_days_loan or book.limit_days_loan,
                year_book or book.year_book,
                synopsis_book or book.synopsis_book or "",
                id_publisher or book.id_publisher,
                isbn_book
            ],
            commit=True
        )
        book = Book.find_book_by_isbn(isbn_book)
        return Book(
            book.id,
            book.isbn_book,
            book.title_book,
            book.limit_days_loan,
            book.year_book,
            book.synopsis_book or "",
            book.id_publisher
        )

    # Deletar livros específicos
    @classmethod
    def delete_book(cls, book_parameter):
        deleted_book = db.execute(
            "DELETE FROM tb_book WHERE isbn_book = %s LIMIT 1;",
            [book_parameter],
            commit=True
        )
        return deleted_book
