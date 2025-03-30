import os
import sqlite3
from datetime import datetime
from config import Config


class DataBase:
    config = Config()
    table_path = f'{os.getcwd()}/db/{config.DB_NAME}'

    def __init__(self):
        self.create_table()

    def current_time(self) -> str:
        current_datetime = datetime.now()
        return current_datetime.strftime("%H:%M:%S - %d:%m:%Y")

    def create_table(self):
        with sqlite3.connect(DataBase.table_path) as db:
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    serial_number INTEGER PRIMARY KEY,
                    mail TEXT,
                    password TEXT,
                    authy_code TEXT,
                    proxy TEXT,
                    logout_result TEXT,
                    auto_result TEXT,
                    cookie_result TEXT,
                    last_action TEXT
                );
            ''')
            db.commit()

    def db_result(self, column: str, account: tuple, text: str = 'Success') -> None:
        with sqlite3.connect(DataBase.table_path) as db:
            cursor = db.cursor()
            query = f''' UPDATE accounts SET {column} = '{text}', last_action = '{self.current_time()}' WHERE serial_number = {account[0]}'''
            cursor.execute(query)

    def get_db_data_auto(self) -> list:
        with sqlite3.connect(DataBase.table_path) as db:
            cursor = db.cursor()
            query = '''SELECT serial_number, mail, password, authy_code FROM accounts'''
            cursor.execute(query)
            rows = cursor.fetchall()
        return rows

    def get_db_fail_accounts_auto(self) -> list:
        with sqlite3.connect(DataBase.table_path) as db:
            cursor = db.cursor()
            query = '''SELECT serial_number, mail, password, authy_code FROM accounts WHERE auto_result LIKE '%Failed_a%' '''
            cursor.execute(query)
            rows = cursor.fetchall()
        return rows

    def get_db_proxy(self, serial_number: str | int) -> str:
        with sqlite3.connect(DataBase.table_path) as db:
            cursor = db.cursor()
            query = f'''SELECT proxy FROM accounts WHERE serial_number = '{serial_number}' '''
            cursor.execute(query)
            rows = cursor.fetchall()
        return rows[0][0]

    def get_db_data_cookie(self) -> list:
        with sqlite3.connect(DataBase.table_path) as db:
            cursor = db.cursor()
            query = '''SELECT serial_number, proxy FROM accounts'''
            cursor.execute(query)
            rows = cursor.fetchall()
        return rows

    def get_db_fail_accounts_cookie(self) -> list:
        with sqlite3.connect(DataBase.table_path) as db:
            cursor = db.cursor()
            query = '''SELECT serial_number, proxy FROM accounts WHERE cookie_result LIKE '%Failed_c%' '''
            cursor.execute(query)
            rows = cursor.fetchall()
        return rows

    def get_db_data_logout(self) -> list:
        with sqlite3.connect(DataBase.table_path) as db:
            cursor = db.cursor()
            query = '''SELECT serial_number FROM accounts'''
            cursor.execute(query)
            rows = cursor.fetchall()
        return rows

    def get_db_fail_accounts_logout(self) -> list:
        with sqlite3.connect(DataBase.table_path) as db:
            cursor = db.cursor()
            query = '''SELECT serial_number FROM accounts WHERE logout_result LIKE '%Failed_l%' '''
            cursor.execute(query)
            rows = cursor.fetchall()
        return rows
