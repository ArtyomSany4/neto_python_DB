import psycopg2


class DataBase:
    def __init__(self):
        with open('token.txt', 'r') as token_file:
            db_password = token_file.read().strip()
        self.password = db_password
        # self.password = 'МЕСТО ПОД ПАРОЛЬ'

    def cursor(self, SQL_query):
        conn = psycopg2.connect(
            database='Python_DB', 
            user='postgres', 
            password=self.password
            )
        with conn.cursor() as cur:
            cur.execute(SQL_query)
            conn.commit()
        
        conn.close()        

# 1. Функция, создающая структуру БД (таблицы). 
    def create_table(self):
        SQL_query = """
        CREATE TABLE IF NOT EXISTS method_tst(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            surname VARCHAR(255),
            email VARCHAR(255)
            );"""
        return self.cursor(SQL_query)
        
# 2.  Функция, позволяющая добавить нового клиента
    def add_client(self):
        name = input('Enter client\'s name: ')
        surname = input('Enter client\'s surname: ')
        email = input('Enter client\'s email: ')
        SQL_query = (
            f'INSERT INTO method_tst(name, surname, email) VALUES'
            f'(\'{name}\', \'{surname}\', \'{email}\');'
            )
        return self.cursor(SQL_query)
        
    
        
# tbl_name = input('Enter table name: ')
test_exemplyar = DataBase()
test_exemplyar.add_client()