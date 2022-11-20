from database.shared import db
import bcrypt
import mysql.connector


class User:
    def __init__(self, name, email, password_hash, phone_number, address, user_type, confirmed_account = False) -> None:
        self.name = name
        self.email = email
        self.__password_hash = password_hash
        self.phone_number = phone_number
        self.address = address
        self.user_type = user_type
        self.confirmed_account = confirmed_account

    @classmethod
    def new(cls, name, email, password: str, phone_number, address, user_type, confirmed_account = False):
        hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        query = '''
        INSERT INTO tb_user(name_user, email_user, password_user, phone_number_user, address_user, id_user_type, confirmed_account)
            values
                (%s, %s, %s, %s, %s, %s, %s);
        '''
        try:
            parameters = [name, email, hash, phone_number, address, user_type, confirmed_account]
            db.execute(query, parameters, commit=True)
            return User(name, email, hash, phone_number, address, user_type)
        except mysql.connector.Error as err:
            return err.errno

    @classmethod
    def find(cls, email):
        query='SELECT * FROM tb_user WHERE email_user = %s'
        user = db.execute(query, [email])[0]
        return User(user.name_user, user.email_user, user.password_user, user.phone_number_user, user.address_user, user.id_user_type, user.confirmed_account)

    def verify_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.__password_hash.encode())

    def confirm_account(self):
        query="UPDATE tb_user SET confirmed_account = b'1' WHERE email_user = %s;"
        parameters=[self.email]
        db.execute(query, parameters, commit=True)
        self.confirmed_account = 1