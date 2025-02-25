# main.py for running the app
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from app import ExpenseTracker

def main():
    app = QApplication(sys.argv)

    window = ExpenseTracker()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

