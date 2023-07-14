# Создайте программу для управления клиентами на Python.

# Требуется хранить персональную информацию о клиентах:

# имя,
# фамилия,
# email,
# телефон.
# Сложность в том, что телефон у клиента может быть не один, а два, три и даже больше. А может и вообще не быть телефона, например, он не захотел его оставлять.

# Вам необходимо разработать структуру БД для хранения информации и несколько функций на Python для управления данными.

# Функция, создающая структуру БД (таблицы).
# Функция, позволяющая добавить нового клиента.
# Функция, позволяющая добавить телефон для существующего клиента.
# Функция, позволяющая изменить данные о клиенте.
# Функция, позволяющая удалить телефон для существующего клиента.
# Функция, позволяющая удалить существующего клиента.
# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
# Функции выше являются обязательными, но это не значит, что должны быть только они. При необходимости можете создавать дополнительные функции и классы.

# Также предоставьте код, демонстрирующий работу всех написанных функций.

# Результатом работы будет .py файл.

# Каркас кода
# import psycopg2

# def create_db(conn):
#     pass

# def add_client(conn, first_name, last_name, email, phones=None):
#     pass

# def add_phone(conn, client_id, phone):
#     pass

# def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
#     pass

# def delete_phone(conn, client_id, phone):
#     pass

# def delete_client(conn, client_id):
#     pass

# def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
#     pass


# with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
#     pass  # вызывайте функции здесь

# conn.close()


import psycopg2
from psycopg2 import sql
from psycopg2.sql import Identifier

conn = psycopg2.connect(
        database = 'Python_DB',
        user = 'postgres',
        password = 'PG_password'    
            )
conn.autocommit = True
        
# 0.1 Функция, создающая курсор. 
def cursor(SQL_query, params = None):
    with conn.cursor() as cur:
        cur.execute(SQL_query, params)
    return 


# 0.2 Функция, дропающая БД .
def drop_db():
    SQL_query = """
TRUNCATE TABLE phone_numbers, clients;
DROP TABLE phone_numbers, clients; 
"""
    return cursor(SQL_query)


# 1. Функция, создающая структуру БД (таблицы).
def create_table():
    SQL_query = """
    CREATE TABLE IF NOT EXISTS clients(
        client_id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        surname VARCHAR(255),
        email VARCHAR(255) UNIQUE
        );
    CREATE TABLE IF NOT EXISTS phone_numbers(
        phone_id SERIAL PRIMARY KEY,
        phone_number CHAR(11) UNIQUE,
        client_id INTEGER REFERENCES clients(client_id)
        );       
    """
    return cursor(SQL_query)


# 2. Функция, позволяющая добавить нового клиента.
def add_client(name, surname, email):
    SQL_query = """
        INSERT INTO clients(name, surname, email)   
        VALUES(%s, %s, %s)
    """
    params = (name, surname, email)
    return cursor(SQL_query, params)

  
# 3. Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(client_id, phone_number):
    SQL_query = """
        INSERT INTO phone_numbers (client_id, phone_number)   
        VALUES(%s, %s)
    """
    params = (client_id, phone_number)
    return cursor(SQL_query, params) 


# 4. Функция, позволяющая изменить данные о клиенте.
def change_client(conn, client_id, name=None, surname=None, email=None, phone_number=None):
    arg_list = {'name': name, 
                'surname': surname, 
                'email': email, 
                'phone_number': phone_number}
    for key, arg in arg_list.items():
        if arg:
            if key == 'phone_number':
                with conn.cursor() as cur:
                    cur.execute(sql("""
                                  UPDATE phone_numbers SET {}=%s WHERE client_id=%s
                        """).format(Identifier(key)), (arg, client_id))
            else:
                with conn.cursor() as cur:
                    cur.execute(sql("""
                                  UPDATE clients SET {}=%s WHERE client_id=%s
                        """).format(Identifier(key)), (arg, client_id))
    return print('Данные изменены успешно.')



# Дропаем базу
# drop_db()
# Проверяем все функции по порядку
# create_table()  

# add_client('John', 'Daw', '123@daw.com')
# add_client('Second', 'Surname2', '222@daw.com')
# add_client('Third', 'Surname3', '333@daw.com')
# add_phone(1, '891111111')
change_client(conn, 1, name = 'Измененный1')