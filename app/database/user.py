from database.shared import db
import bcrypt
import mysql.connector


class User:
    def __init__(self, name, email, password_hash, phone_number, address, user_type) -> None:
        self.name = name
        self.email = email
        self.__password_hash = password_hash
        self.phone_number = phone_number
        self.address = address
        self.user_type = user_type

    @classmethod
    def new(cls, name, email, password: str, phone_number, address, user_type):
        hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        query = '''INSERT INTO tb_user(name_user, email_user, password_user, phone_number_user, address_user, id_user_type)
            values
                (%s, %s, %s, %s, %s, %s);
        '''
        try:
            parameters = [name, email, hash,
                          phone_number, address, user_type]
            db.execute(query, parameters, commit=True)
            return User(name, email, hash, phone_number, address, user_type)
        except mysql.connector.Error as err:
            return err.errno

    @classmethod
    def find(cls, email):
        user = db.execute(
            'SELECT * FROM tb_user WHERE email_user = %s', [email])[0]
        return User(user.name_user, user.email_user, user.password_user, user.phone_number_user, user.address_user, user.id_user_type)

    def verify_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.__password_hash.encode())
