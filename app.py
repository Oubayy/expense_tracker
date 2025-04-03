from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit, QComboBox,
                             QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QTableWidgetItem, QHeaderView)

from PyQt6.QtCore import QDate, Qt
from unicodedata import category

from database import fetch_expenses, add_expenses, delete_expenses


class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.load_table_data()

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

        self.add_button.clicked.connect(self.add_expense)
        self.del_button.clicked.connect(self.delete_expense)

        self.apply_styles()

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

    def apply_styles(self):
        self.setStyleSheet("""
                            QWidget{
                                background-color: 3e3e9f2;
                                font-family: Arial, sans-serif;
                                font-size: 14px;
                                color:#333;
                            }
                            
                            QLabel{
                                font-size: 16px;
                                font-weight: bold;
                                color: #2c3e90;
                                padding: 5px;
                            }
                            
                            QLineEdit, QComboBox, QDateEdit{
                                background-color: #fff;
                                font-size: 14px;
                                color: #333;
                                border: 1px solid 3b0bfc6;
                                border-radius: 15px;
                                padding: 5px;
                            }
                            
                            QlineEdit:hover, QComboBox:hover, QDateEdit:hover{
                                border: 1px solid #4caf50;
                            }
                            
                            QlineEdit:focus, QComboBox:focus, QDateEdit:focus{
                                border: 1px solid #2a9d8f;
                                background-color: #f5f9fc;
                            }
                            
                            QTableWidget{
                                background-color: #fff;
                                alternate-background-color: #f2f7fb;
                                gridline-color: #c0c9d0;
                                selection-background-color: #4caf50;
                                selection-color: white;
                                font-size: 14px;
                                border 1px solid #cfd9e1;
                            }
                           """)

    def populate_dropdown(self):
        categories = ["Snacks", "Sport", "School", "Personal", "Other"]
        self.dropdown.addItems(categories)

    def load_table_data(self):
        """
        Takes information from the db and project it into our application
        (should be called each time we make a change to the db)
        :return:
        """
        expenses = fetch_expenses()
        self.table.setRowCount(0)
        for row_index, expense in enumerate(expenses):
            self.table.insertRow(row_index)
            for col_index, data in enumerate(expense):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

    # We need a function that collects date, category, amount and description and then calls add_expenses

    def add_expense(self):
        date = self.date_box.date().toString("dd-mm-yyyy")
        category = self.dropdown.currentText() # QComboBox
        amount = self.amount.text() # QLineEdit
        description = self.description.text()

        # Checks:
        if not amount or not description:
            QMessageBox.warning(self, "Input Error", "Amount and Description can not be empty")
            return

        if add_expenses(date, category, amount, description):
            self.load_table_data() # Since we are making a change to the db, load should be called
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Error", "Failed to add expense")

    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

    def delete_expense(self):
        # We want to click on a row in the table, get the ID and then delete it from the db
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Oops", "You haven't selected a row to delete.")
            return

        expense_id = int(self.table.item(selected_row, 0).text())
        confirmation = QMessageBox.question(self, "Confirm", "Are you sure that you want to delete this expense?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirmation == QMessageBox.StandardButton.Yes and delete_expenses(expense_id):
            self.load_table_data()
