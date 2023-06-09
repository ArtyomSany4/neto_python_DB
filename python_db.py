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

    
    def select_meth(self, select):
        # client_id = input('Enter client_id: ')
        select = select 
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
            phone_number BIGINT UNIQUE,
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
        select = f'SELECT name FROM clients WHERE id = {client_id}'
        resp = self.select_meth(select)
        if resp == None:
            print(f'Client with client_id = {client_id} not found. Enter a correct client_id')
        else:
            phone_number = input('Enter client phone_number: ')
            SQL_query = (
                f'INSERT INTO phone_numbers(client_id, phone_number) VALUES'
                f'(\'{client_id}\', \'{phone_number}\');'
                )
            self.cursor(SQL_query)
            print(f'Номер телефона {phone_number} успешно добавлен клиенту с ИД {client_id}!')

# 4.  Функция, позволяющая изменить данные о клиенте
    def updt_clnt_data(self):
        route = input("""
What do you want to change?
Enter your choice: 
1 - name, 2 - surname, 3 - email.
            """)
        if int(route) == 1:
            client_id = input('Enter client_id: ') 
            select = f'SELECT name FROM clients WHERE id = {client_id}'
            if self.select_meth(select) == None:
                print(f'Client with client_id = {client_id} not found. Enter a correct client_id')
            else:
                name = input('Enter client\'s new name: ')
                updt = (
                    f'UPDATE clients\n'
                    f'SET name = \'{name}\'\n'
                    f'WHERE id = {client_id};'
                    )
                
        if int(route) == 2:
            client_id = input('Enter client_id: ') 
            select = f'SELECT name FROM clients WHERE id = {client_id}'
            if self.select_meth(select) == None:
                print(f'Client with client_id = {client_id} not found. Enter a correct client_id')
            else:
                surname = input('Enter client\'s new surname: ')
                updt = (
                    f'UPDATE clients\n'
                    f'SET name = \'{surname}\'\n'
                    f'WHERE id = {client_id};'
                    )  

        if int(route) == 3:
            client_id = input('Enter client_id: ') 
            select = f'SELECT name FROM clients WHERE id = {client_id}'
            if self.select_meth(select) == None:
                print(f'Client with client_id = {client_id} not found. Enter a correct client_id')
            else:
                email = input('Enter client\'s new email: ')
                updt = (
                    f'UPDATE clients\n'
                    f'SET email = \'{email}\'\n'
                    f'WHERE id = {client_id};'
                    )
        self.cursor(updt)
        return print('Data was updated successfully.')

# 5. Функция, позволяющая удалить телефон для существующего клиента.
    def phone_del(self):
        client_id = input('Enter client_id: ') 
        select = f'SELECT name FROM clients WHERE id = {client_id}'
        if self.select_meth(select) == None:
            print(f'Client with client_id = {client_id} not found. Enter a correct client_id')
        else:
            delete = (
                    f'DELETE from phone_numbers\n'
                    f'WHERE client_id = {client_id};'
                )
        self.cursor(delete)
        return print('Phone number successfully deleted.')



# 6. Функция, позволяющая удалить существующего клиента.
    def client_del(self):
        client_id = input('Enter client_id: ') 
        select = f'SELECT name FROM clients WHERE id = {client_id}'
        if self.select_meth(select) == None:
            print(f'Client with client_id = {client_id} not found. Enter a correct client_id')
        else:
            select = f'SELECT * FROM phone_numbers WHERE client_id = {client_id}'
            delete = (
                    f'DELETE from clients\n'
                    f'WHERE id = {client_id};'
                )
            if self.select_meth(select) == None:
                self.cursor(delete)
            else:
                self.phone_del()
                self.cursor(delete)              
        return print('Client successfully deleted.')

# 7. Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
    def multy_select(self, name = '*', surname = '*', email = '*', phone_number = '*'):
        
        

test_exemplyar = DataBase()
# 1. Функция, создающая структуру БД (таблицы).        
# test_exemplyar.create_table()

# 2.  Функция, позволяющая добавить нового клиента
# test_exemplyar.add_client()

# 3. Функция, позволяющая добавить телефон для существующего клиента.
# test_exemplyar.add_clnt_phone_numb()

# 4.  Функция, позволяющая изменить данные о клиенте
# test_exemplyar.updt_clnt_data()

# 5. Функция, позволяющая удалить телефон для существующего клиента.
# test_exemplyar.phone_del()

# 6. Функция, позволяющая удалить существующего клиента.
test_exemplyar.client_del()