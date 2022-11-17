from shared import db 
import mysql.connector
from .book import Book

class Category:
    def __init__(self, id:int, name:str) -> None:
        self.id = id
        self.name = name

    @classmethod        
    def list_category (cls):
        list_category = db.execute('SELECT * FROM tb_category;')
        return Book(list_category)


    @classmethod
    def find_category(cls, name):
        especific_category = db.execute(
            '''SELECT * FROM tb_category 
                WHERE name_category 
                    LIKE '%{%s}%';''', [name])[0]
        return Category(especific_category.name)
    

    @classmethod
    def insert_category(cls, name):
        query = '''INSERT INTO tb_category(name_category) 
            values 
	            (%s);
        '''
        try:
            parameters = [name]
            db.execute(query, parameters, commit=True)
            return Category(name)
        except mysql.connector.Error as err:
            return err.errno


    # @classmethod
    # def alter_category


    # @classmethod
    # def delete_category
    