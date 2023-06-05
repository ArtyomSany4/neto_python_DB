import psycopg2



class DataBase:
    def __init__(self):
        with open('token.txt', 'r') as token_file:
            db_password = token_file.read().strip()
        self.password = db_password

    def create_table(self, tbl_name):
        conn = psycopg2.connect(
            database='Python_DB', 
            user='postgres', 
            password=self.password
            )
        with conn.cursor() as cur:
            cur.execute(f'CREATE TABLE IF NOT EXISTS {tbl_name}(id SERIAL PRIMARY KEY);')
            conn.commit()
        
        conn.close()
        
tbl_name = input('Enter table name: ')
test_exemplyar = DataBase()
test_exemplyar.create_table(tbl_name)


    # def __init__(self, token: str):
    #     self.token = token

    # def get_headers(self):
    #     return {
    #         'Content-Type': 'application/json',
    #         'Authorization': 'OAuth {}'.format(self.token)
    #     }