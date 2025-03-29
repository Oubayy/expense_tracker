#
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

def init_db(db_name): # to initialize the database
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(db_name)

    if not database.open():
        return False # Error, we can't run the app without a database

    query = QSqlQuery()
    query.exec("""
               CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTO INCREMENT,
                    date TEXT,
                    category TEXT,
                    amount REAL,
                    description TEXT
               )
               """)

    return True

def fetch_expenses():
    query = QSqlQuery("SELECT * FROM expenses ORDER BY date DESC")
    expenses = []
    while query.next():
        expenses.append([query.value(i)] for i in range(5)) # We have 5 columns
    return expenses

def add_expenses():
    pass

def delete_expenses():
    pass

# We now need 3 SQL functions for fetching, adding and deleting in order to interact with the db