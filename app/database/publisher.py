from shared import db 
import mysql.connector
from .book import Book

class Publisher:
    def __init__(self, id:int, name:str) -> None:
        self.id = id
        self.name = name


    @classmethod        
    def list_publisher (cls):
        list_publisher = db.execute('SELECT * FROM tb_publisher;')
        return Book(list_publisher)
    
    
    @classmethod
    def insert_publisher(cls, name):
        new_publisher = '''INSERT INTO tb_publisher(name_publisher) 
            VALUES
	            (%s);
        '''
        try:
            parameters = [name]
            db.execute(new_publisher, parameters, commit=True)
            return Publisher(name)
        except mysql.connector.Error as err:
            return err.errno

    @classmethod
    def find_publisher(cls, name):
        especific_publisher = db.execute(
            'SELECT * FROM tb_publisher WHERE name_publisher = %s;', [name])[0]
            # TODO - VERIFY - Sintax for non-exact data inserted 
                # 'SELECT * FROM tb_publisher WHERE name_publisher LIKE '%{%s}%';'
        return Publisher(especific_publisher.name_publisher)

    @classmethod
    def find_book_by_publisher(cls, name):
        especific_book = db.execute(
        '''SELECT * FROM tb_book 
            WHERE id_publisher = 
                (SELECT id_publisher 
                WHERE name_publisher LIKE '%{%s}%');''', [name])
        return Book(especific_book.name)

    # @classmethod
    # def alter_publisher

    # @classmethod
    # def delete_publisher


    