'''
Database management module. Integrates with the front-end (PySimpleGUI app)
'''

# external packages
import sqlite3 as sqlite
import pandas as pd
import random

# local imports
if __name__ == "__main__":
    from definitions import *
    from default_ops import gui_keys_to_write_to_db
else:
    from utils.definitions import *
    from utils.default_ops import gui_keys_to_write_to_db

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

        print(row_dict)

        # give the record an ID
        insert_cols.append('Project_ID')
        
        valid_id = True
        while valid_id:
            project_id = random.randint(100000, 999999)
            if project_id not in self.__get_project_ids():
                valid_id = False
        
        #print(project_id)
        insert_vals.append(project_id)
        
        for column, value in row_dict.items():
            print(column)
            if column in gui_keys_to_write_to_db:
                 insert_cols.append(column)
                 insert_vals.append(value)

        print(insert_cols)

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

    def __get_project_ids(self):
        sql = 'SELECT Project_ID from projects'
        df = pd.read_sql(sql, con=self.connection)
        return list(df['Project_ID'].unique()) # they already should be unique

    def get_project_data_for_lbox(self):
        sql = 'SELECT Project_ID, Program, Workstream, Project_Name from projects'
        df = pd.read_sql(sql, con=self.connection)

        rows = []
        for row in zip(df['Project_ID'], df['Program'], df['Workstream'], df['Project_Name']):
            rows.append(row)
        
        return rows
    

if __name__ == "__main__":
    db = Database()
    print(db.get_project_data_for_lbox())
