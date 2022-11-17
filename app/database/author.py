from shared import db 
import mysql.connector
from .book import Book

class Author:
    def __init__(self, id:int, name:str) -> None:
        self.id = id
        self.name = name


    @classmethod        
    def list_author (cls):
        list_authors = db.execute('SELECT * FROM tb_author;')
        return Book(list_authors)


    @classmethod
    def find_author(cls, name):
        author = db.execute(
            '''SELECT * FROM tb_author 
                WHERE name_author 
                    LIKE '%{%s}%';''', [name])[0]
        return Author(author.name)


    @classmethod
    def insert_author(cls, name):
        new_author = '''INSERT INTO tb_author(name_author) 
            VALUES 
	            (%s);
        '''
        try:
            parameters = [name]
            db.execute(new_author, parameters, commit=True)
            return Author(name)
        except mysql.connector.Error as err:
            return err.errno


    # @classmethod
    # def alter_author


    # @classmethod
    # def delete_author

    