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

# We now need 3 SQL functions for fetching, adding and deleting in order to interact with the db

def fetch_expenses():
    """
    Every time we load the app or make a change to the database this function gets called to update the table visually
    :return: a list
    """
    query = QSqlQuery("SELECT * FROM expenses ORDER BY date DESC")
    expenses = []
    while query.next():
        row = [[query.value(i)] for i in range(5)]
        # expenses.append([[query.value(i)] for i in range(5)]) # We have 5 columns
        expenses.append(row)
    return expenses

def add_expenses(date, category, amount, description):
    query = QSqlQuery()
    query.prepare("""
                  INSERT INTO expenses (date, category, amount, description)
                  VALUES (?, ?, ?, ?)
                  """) # prepare to send data off into the db
    # question marks need a binding value
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)

    return query.exec()

def delete_expenses(expense_id):
    query = QSqlQuery()
    query.prepare("DELETE FROM expenses WHERE id = ?")
    query.addBindValue(expense_id)
    return query.exec()
