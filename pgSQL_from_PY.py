import psycopg2
from psycopg2.sql import SQL, Identifier


with open('token.txt', 'r') as token_file:
    password = token_file.read().strip()
# password = 'МЕСТО ПОД ПАРОЛЬ'

conn = psycopg2.connect(
    database='Python_DB', 
    user='postgres', 
    password=password
    )

def cursor(SQL_query):
    with conn.cursor() as cur:
        cur.execute(SQL_query)
        conn.commit()

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

        
# 2.  Функция, позволяющая добавить нового клиента
def add_client(name, surname, email):
    with conn.cursor() as cur:
        cur.execute("""
                     INSERT INTO clients(name, surname, email) VALUES(%s, %s, %s);
            """, (name, surname, email))
        conn.commit()
    print(f'Клиент {surname} успешно добавлен!')
    return 

# 3. Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
                     INSERT INTO phone_numbers(client_id, phone_number) VALUES(%s, %s);
            """, (client_id, phone_number))
        conn.commit()
    print(f'Номер телефона {phone_number} успешно добавлен клиенту с ИД {client_id}!')

# 4.  Функция, позволяющая изменить данные о клиенте.
def change_client(client_id, name=None, surname=None, email=None, phone_number=None):
    arg_list = {'name': name, 'surname': surname, 'email': email, 'phone_number': phone_number}
    for key, arg in arg_list.items():
        if arg:
            if key == 'phone_number':
                with conn.cursor() as cur:
                    cur.execute(SQL("""
                                  UPDATE phone_numbers SET {}=%s WHERE client_id=%s
                        """).format(Identifier(key)), (arg, client_id))
                    conn.commit()
            else:
                with conn.cursor() as cur:
                    cur.execute(SQL("""
                                  UPDATE clients SET {}=%s WHERE client_id=%s
                        """).format(Identifier(key)), (arg, client_id))
                    conn.commit()

                    
# 5. Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone_number(client_id, phone_number):
    SQL_query = (
            f'DELETE from phone_numbers\n'
            f'WHERE client_id = {client_id}\n'
            f'AND phone_number = \'{phone_number}\';'
        )
    cursor(SQL_query)
    return print('Phone number successfully deleted.')

# 6. Функция, позволяющая удалить существующего клиента.
def delete_client(client_id):
    with conn.cursor() as cur:
        cur.execute(
            f'DELETE from phone_numbers\n'
            f'WHERE client_id = {client_id}\n;'
            f'DELETE from clients\n'
            f'WHERE client_id = {client_id}\n'
            )
        conn.commit()
    print(f'Клиент с ИД {client_id} успешно удален!')

# 7. Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def find_client(name=None, surname=None, email=None, phone_number=None):
    arg_list = {'name': name, 'surname': surname, 'email': email, 'phone_number': phone_number}
    for key, arg in arg_list.items():
        if arg:
            with conn.cursor() as cur:
                cur.execute(SQL("""
                              SELECT * FROM clients c
                              JOIN phone_numbers pn
                              ON c.client_id = pn.client_id 
                              WHERE {}=%s
                    """).format(Identifier(key)), (arg))
                conn.commit()
                
    # with conn.cursor() as cur:
    #     cur.execute("""
    #                 SELECT * FROM clients c
    #                 LEFT JOIN phone_numbers pn
    #                 ON c.client_id = pn.client_id
    #                 WHERE 
    #                 c.name = %s 
    #                 OR c.surname = %s 
    #                 OR c.email = %s
    #                 OR pn.phone_number = %s;
    #                       """, (name, surname, email, phone_number)
    #                       )
    #     print(cur.fetchall())
    

# drop_db()
# create_table() 
# add_client('Июль', 'Июлев', '123@ex.com')
# add_client('Second', 'Clientfio', '222@ex.com')
# add_phone(1, '89372275447')
# add_phone(2, '89372275446')


# print(change_client('1', name='Сменщиков', phone_number='123433'))
# delete_phone_number(1, '123433')
# delete_client(2)
find_client('Июль')


# with psycopg2.connect(database="Python_DB", user="postgres", password=password) as conn:
#     print(change_client2('1', name='тестов', email='1243'))

conn.close()