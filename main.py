# main.py for running the app
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from database import init_db
from app import ExpenseTracker

def main():
    app = QApplication(sys.argv)

    if not init_db("expense_tracker.db"):
        QMessageBox.critical(None, "Error", "Could not load your database.")
        sys.exit(1) # The app exits after 1 sec

    window = ExpenseTracker()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

