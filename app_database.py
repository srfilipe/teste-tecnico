"""
    Connects to the SQL Server database using pyodbc
"""

import pyodbc

SERVER = 'localhost\\SQLEXPRESS'
DATABASE = 'tech_test'
TRUSTED_CONNECTION = 'yes'

connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection={TRUSTED_CONNECTION}'

def get_connection():
    try:
        conn = pyodbc.connect(connectionString, timeout=5)
        return conn
    except pyodbc.Error as e:
        print("Connection failed...", e.args[1])
        raise