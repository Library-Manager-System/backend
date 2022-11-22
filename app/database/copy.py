from database.shared import db
import mysql.connector


class Copy:
    def __init__(self, id: int, code_copy: str, available_copy: bool, id_book: int, address_copy: str, title: str = None, isbn: str = None) -> None:
        self.id = id
        self.code_copy = code_copy
        self.available_copy = available_copy
        self.id_book = id_book
        self.address_copy = address_copy
        self.title = title
        self.isbn = isbn

    @classmethod
    def new(cls, code_copy: str, available_copy: bool, id_book: int, address_copy: str ):
        query = """
        INSERT INTO tb_copy(code_copy, available_copy, id_book, address_copy) VALUES (%s, %s, %s, %s);
        """
        parameters = [code_copy, available_copy, id_book, address_copy]
        try:
            copy_id = db.execute(query, parameters, commit=True)
            return Copy(copy_id, code_copy, available_copy, id_book, address_copy)
        except mysql.connector.Error as err:
            return err.errno

    @classmethod
    def find(cls, id):
        query = """
        SELECT * FROM vw_copy WHERE id_copy = %s;
        """
        parameters = [id]
        copy = db.execute(query, parameters)
        return Copy(copy.id_copy, copy.code_copy, copy.available_copy, copy.id_book, copy.address_copy)

    @classmethod
    def find_all_copy_by_isbn(cls, isbn):
        query = """
        SELECT * FROM vw_copy WHERE isbn_book = %s;
        """