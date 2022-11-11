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
                book.syphosis_book if book.syphosis_book else "",
                book.id_publisher
            ))
        return books


    # Consultar livros específicos
        # TODO - receber algum dos 3 tipos de dado para mostrar pesquisa de livros
        # TODO - permitir quantos livros mostrar (ex.: 'LIMIT 4,5')
    @classmethod
    def find_book_by_isbn_or_title(cls, book_parameter):
        especific_book = db.execute(
        '''SELECT * FROM tb_book
            WHERE isbn_book = %s'
            OR
            title_book LIKE '%{%s}%';''', [book_parameter, book_parameter])
        return Book(especific_book.book_parameter)


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
        # Opção 1: alterar algum dado específico
        # Opção 2: alterar todos os dados, podendo colocar opção "não alterar/manter dado anterior"
        # Lógica:
            # Receber entrada do usuário sobre qual livro deseja alterar dados (por título ou isbn)
            # Mostrar dados do livro
            # O usuário colocar campos que deseja alterar do livro
            # Perguntar se deseja realmente alterar
            # Alterar dados do livro
    # @classmethod
    # def alter_book(cls, book_parameter):
    #     altered_book = db.execute(
    #         '''ALTER TABLE * FROM tb_book WHERE isbn_book = %s OR title_book = %s;''', [book_parameter, book_parameter])[0]
    #     return Book(altered_book.book_parameter)


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