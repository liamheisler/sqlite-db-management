'''
Database management module. Integrates with the front-end (PySimpleGUI app)
'''

# external packages
import sqlite3 as sqlite
import pandas as pd
import random

# local imports
from utils.definitions import *

class Database:
    def __init__(self) -> None:
        self.__db_path = DB_FILE
        self.connection = sqlite.connect(DB_FILE)
    
    def disconnect(self) -> None:
        self.__sqlite_connection.disconnect()
        
    def insert_row(self, row_dict):
        # preparing the query
        insert_cols = []
        insert_vals = []

        # give the record an ID
        insert_cols.append('Project_ID')
        
        # TODO finish and test
        valid_id = True
        while valid_id:
            project_id = random.randint(100000, 999999)
            if project_id not in self._get_project_ids():
                valid_id = False
        
        print(project_id)
        insert_vals.append(project_id)
        
        for column, value in row_dict.items():
            if "tab" not in column:
                 insert_cols.append(column)
                 insert_vals.append(value)

        print(insert_vals)

        insert_cols_str = ', '.join([f'"{column}"' for column in insert_cols if "tab" not in column])
        placeholders = ', '.join(['?'] * len(insert_vals))  # placeholders for values
        
        # generate the query
        sql = f'INSERT INTO projects({insert_cols_str}) VALUES ({placeholders})'

        # Executing the SQL command
        actually_enter_row = True

        if actually_enter_row:
            try:
                cursor = self.connection.cursor()
                print(sql)
                cursor.execute(sql, tuple(insert_vals))  # parameter substitution for values
                self.connection.commit()  # committing the changes
                
                return True
            except sqlite.Error as e:
                print(f"An error occurred: {e}")
                return False
            finally:
                cursor.close() # good practice
        else:
            print("testing mode: ", sql)
            return False
    
    # getter methods
    def get_project_data(self):
        sql = 'SELECT * FROM projects' # project
        return pd.read_sql(sql, con=self.connection)

    def _get_project_ids(self):
        sql = 'SELECT Project_ID from projects'
        df = pd.read_sql(sql, con=self.connection)
        return list(df['Project_ID'].unique()) # they already should be unique