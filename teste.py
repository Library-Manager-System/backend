import mysql.connector
from dotenv import load_dotenv
import os

class Database:
    def __init__(self, user , password, host, database):
        self.cnx = mysql.connector.connect(
                user = user,
                password = password,
                host = host,
                database = database
                )

    def __del__(self):
        self.cnx.close()

    def execute(self, query, parameters=[], commit=False):
        cs = self.cnx.cursor(named_tuple=True)
        cs.execute(query, parameters)
        if commit:
            result = cs.lastrowid
            self.cnx.commit()
        else:
            result = cs.fetchall()
        cs.close()
        return result

load_dotenv()

db = Database(user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'), database=os.getenv('DB_NAME'))

class Loan:
    def __init__(self, id_loan, id_user, id_copy, dt_expected_collect, dt_loan, dt_expected_devolution_loan, approved_loan, dt_real_devolution_loan=None) -> None:
        self.id_loan = id_loan
        self.id_user = id_user
        self.id_copy = id_copy
        self.dt_expected_collect = dt_expected_collect
        self.dt_loan = dt_loan
        self.dt_expected_devolution_loan = dt_expected_devolution_loan
        self.dt_real_devolution_loan = dt_real_devolution_loan
        self.approved_loan = approved_loan
            
    @classmethod
    def new(cls, id_user, id_copy, dt_expected_collect, dt_loan, dt_expected_devolution_loan, approved_loan):
        query = """
            INSERT INTO tb_loan(id_user, id_copy, dt_expected_collect, dt_loan, dt_expected_devolution_loan, approved_loan)
                VALUES (%s, %s, %s, %s, %s, b'%s');
        """
        try:
            parameters =[id_user, id_copy, dt_expected_collect, dt_loan, dt_expected_devolution_loan, approved_loan]
            db.execute(query, parameters, commit=True)
            return Loan(id_user, id_copy, dt_expected_collect, dt_loan, dt_expected_devolution_loan, approved_loan)
        except mysql.connector.Error as err:
            return err.errno

    @classmethod
    def find(cls, id_loan):
        loan = db.execute('SELECT * FROM tb_loan WHERE id_loan = %s', [id_loan])[0]
        return Loan(loan.id_loan, loan.id_user, loan. id_copy, loan.dt_expected_collect, loan.dt_loan, 
                    loan.dt_expected_devolution_loan, loan.approved_loan, loan.dt_real_devolution_loan)
        
    def approve_loan(self):
        query = "UPDATE tb_loan SET approved_loan = b'1' WHERE id_loan = 1;"
        db.execute(query, commit=True)
        self.approve_loan = 1

l = Loan.find(1)
print(l.id_copy, l.approve_loan)
l.approve_loan()