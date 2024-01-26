'''
Database management module. Integrates with the front-end (PySimpleGUI app)
'''

# external packages
import sqlite3 as sqlite
import pandas as pd

# local imports
from utils.definitions import *

class Database:
    def __init__(self) -> None:
        self.__db_path = DB_FILE
        self.connection = sqlite.connect(DB_FILE)
    
    def disconnect(self) -> None:
        self.__sqlite_connection.disconnect()

    def get_project_data(self):
        sql = 'SELECT FROM testing' # project
        return pd.read_sql(sql, con=self.connection)
    
    def insert_row(self, row_dict):
        # Preparing the SQL query. We need to handle the keys and values separately.
        columns = ', '.join([f'"{column}"' for column in row_dict.keys()])
        placeholders = ', '.join(['?'] * len(row_dict))  # placeholders for values
        sql = f'INSERT INTO testing ({columns}) VALUES ({placeholders})'

        # Values as a tuple
        values = tuple(row_dict.values())

        # Executing the SQL command
        try:
            cursor = self.connection.cursor()
            print(sql)
            cursor.execute(sql, values)  # Using parameter substitution for values
            self.connection.commit()  # Committing the changes
        except sqlite.Error as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()  # It's a good practice to close the cursor

        print(row_dict)