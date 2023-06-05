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
        
    def create_table(self):
        SQL_query = """
        CREATE TABLE IF NOT EXISTS method_tst(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            surname VARCHAR(255),
            email VARCHAR(255)
            );"""
        return self.cursor(SQL_query)
        
        
        
        
# tbl_name = input('Enter table name: ')
test_exemplyar = DataBase()
test_exemplyar.create_table()