from database.shared import db
import mysql.connector

class Book:
    def __init__(self, id:int, isbn_book:str, title_book:str, limit_days_loan:int, year_book:int, synopsis_book:str, id_publisher:int) -> None:
        self.id = id
        self.isbn_book = isbn_book
        self.title_book = title_book
        self.limit_days_loan = limit_days_loan
        self.year_book = year_book
        self.synopsis_book = synopsis_book
        self.id_publisher = id_publisher


    # Consultar todos os livros
    @classmethod
    def list_book(cls):
        list_book = db.execute('SELECT * FROM tb_book;')
        books = []
        for book in list_book:
            books.append(Book(
                book.id_book,
                book.isbn_book,
                book.title_book,
                book.limit_days_loan,
                book.year_book,
                book.synopsis_book or "",
                book.id_publisher
            ))
        return books


    # Consultar livros específicos
    @classmethod
    def find_book_by_data(cls, book_parameter):
        list_book = db.execute(
            '''SELECT * FROM tb_book
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
                book.id_publisher
            ))
        return books


    @classmethod
    def find_book_by_isbn(cls, isbn: str):
        specific_book = db.execute(
            '''
            SELECT * FROM tb_book
            WHERE isbn_book = %s;
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
            specific_book.id_publisher
        )


    # Adicionar livros
    @classmethod
    def insert_book(cls, isbn_book, title_book, limit_days_loan, year_book, synopsis_book, id_publisher):
        new_book = '''INSERT INTO tb_book(isbn_book, title_book, limit_days_loan, year_book, synopsis_book, id_publisher)
            VALUES
                (%s, %s, %s, %s, %s, %s);
        '''
        try:
            parameters = [isbn_book, title_book, limit_days_loan, year_book, synopsis_book, id_publisher]
            db.execute(new_book, parameters, commit=True)
            return Book(isbn_book, title_book, limit_days_loan, year_book, synopsis_book, id_publisher)
        except mysql.connector.Error as err:
            return err.errno


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
        # Lógica:
            # Receber entrada do usuário sobre qual livro deseja deletar dados (por título ou isbn)
            # Mostrar dados do livro
            # Perguntar se deseja realmente deletar
            # Deletar dados do livro
    # @classmethod
    # def delete_book(cls, book_parameter):
    #     deleted_book = db.execute(
    #         'DELETE * FROM tb_book WHERE title_book = %s OR isbn_book = %s;', [book_parameter, book_parameter])[0]
    #     return Book(deleted_book.book_parameter)