import mysql.connector

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
            self.cnx.commit()
            result = cs.lastrowid
        else:
            result = cs.fetchall()
        cs.close()
        return result