from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit, QComboBox,
                             QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QTableWidgetItem, QHeaderView)

from PyQt6.QtCore import QDate, Qt
from database import fetch_expenses, add_expenses, delete_expenses


class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()

    def settings(self):
        self.setGeometry(300, 300, 525, 475)
        self.setWindowTitle("Expense Tracker")


    # Design
    def initUI(self):
        # We need to create an object for everything that we want to see in the app
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())

        self.dropdown = QComboBox() # So that the user can categorise their expenses

        self.amount = QLineEdit()

        self.description = QLineEdit()

        self.add_button = QPushButton("Add Expense")
        self.del_button = QPushButton("Delete Expense")

        # We cannot see the database, it is behind the scenes
        self.table = QTableWidget(0,5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Description"])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) # Edits table width

        self.populate_dropdown()

        self.setup_layout()

    def setup_layout(self):
        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        # Row 1
        row1.addWidget(QLabel("Date"))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel("Category"))
        row1.addWidget(self.dropdown)

        # Row 2
        row2.addWidget(QLabel("Amount"))
        row2.addWidget(self.amount)
        row2.addWidget(QLabel("Description"))
        row2.addWidget(self.description)

        # Row 3
        row3.addWidget(self.add_button)
        row3.addWidget(self.del_button)

        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)
        master.addWidget(self.table)

        self.setLayout(master)

    def populate_dropdown(self):
        categories = ["Snacks", "Sport", "School", "Personal", "Other"]
        self.dropdown.addItems(categories)
