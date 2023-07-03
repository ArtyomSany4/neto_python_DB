import psycopg2
with open('token.txt', 'r') as token_file:
    db_password = token_file.read().strip()
password = db_password
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
    conn.close() 
    
# 1. Функция, создающая структуру БД (таблицы). 
def create_table():
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
    return cursor(SQL_query)

# 2.  Функция, позволяющая добавить нового клиента
def add_client():
    name = input('Enter client\'s name: ')
    surname = input('Enter client\'s surname: ')
    email = input('Enter client\'s email: ')
    SQL_query = (
        f'INSERT INTO clients(name, surname, email) VALUES'
        f'(\'{name}\', \'{surname}\', \'{email}\');'
        )
    print(f'Клиент {surname} успешно добавлен!')
    return cursor(SQL_query)



# 7. Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    SQL_query = (
        """SELECT ID FROM USERS WHERE EMAIL = %s OR
                         USERNAME = %s;
                         """)
    
        # cur.execute("""
        # SELECT id FROM course WHERE name=%s;
        # """, ("Python",))  # хорошо, обратите внимание на кортеж
        # print(cur.fetchone())
    
    
    

    
    
conn.close()        