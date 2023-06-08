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

    
    def clnt_srch_query(self, client_id):
        # client_id = input('Enter client_id: ')
        client_id = client_id
        select = f'SELECT name FROM clients WHERE id = {client_id}'
        conn = psycopg2.connect(
            database='Python_DB', 
            user='postgres', 
            password=self.password
            )
        with conn.cursor() as cur:
            cur.execute(select)
            fetch = cur.fetchone()
            print(fetch)
        # conn.close()  
        return fetch

# 1. Функция, создающая структуру БД (таблицы). 
    def create_table(self):
        SQL_query = """
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            surname VARCHAR(255),
            email VARCHAR(255) UNIQUE
            );
        CREATE TABLE IF NOT EXISTS phone_numbers(
            id SERIAL PRIMARY KEY,
            phone_number INTEGER UNIQUE,
            client_id INTEGER REFERENCES clients(id)
            );
        
        
        """
        return self.cursor(SQL_query)
        
# 2.  Функция, позволяющая добавить нового клиента
    def add_client(self):
        name = input('Enter client\'s name: ')
        surname = input('Enter client\'s surname: ')
        email = input('Enter client\'s email: ')
        SQL_query = (
            f'INSERT INTO clients(name, surname, email) VALUES'
            f'(\'{name}\', \'{surname}\', \'{email}\');'
            )
        print(f'Клиент {surname} успешно добавлен!')
        return self.cursor(SQL_query)
        
# 3. Функция, позволяющая добавить телефон для существующего клиента.
    def add_clnt_phone_nmbr(self):
        client_id = input('Enter client_id: ')
        resp = self.clnt_srch_query(client_id)
        if resp != None:
            phone_number = input('Enter client phone_number: ')
            SQL_query = (
                f'INSERT INTO phone_numbers(client_id, phone_number) VALUES'
                f'(\'{client_id}\', \'{phone_number}\');'
                )
            self.cursor(SQL_query)
        print(f'Номер телефона {phone_number} успешно добавлен клиенту с ИД {client_id}!')






     
# tbl_name = input('Enter table name: ')
test_exemplyar = DataBase()

# test_exemplyar.add_client()
test_exemplyar.add_clnt_phone_nmbr()
# test_exemplyar.clnt_search_query()
# test_exemplyar.add_clnt_phone_numb()
# test_exemplyar.create_table()