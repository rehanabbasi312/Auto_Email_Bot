
import pyodbc
from config import db_host, db_user, db_password, db_database

# DATABASE CONNECTIVITY
def ReturnDatabaseConnection():
    try:
        conn_str = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={db_host};DATABASE={db_database};UID={db_user};PWD={db_password}"
        return pyodbc.connect(conn_str)
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


# RETURN DATABASE OBJECT
def ReturnDatabaseObject():
    mydb: object = ReturnDatabaseConnection()
    return mydb
    