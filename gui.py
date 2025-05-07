"""
Budget Tracker GUI using PyQt6
Author: Camryn Klintworth
Sources:
- PyQt6 documentation: https://doc.qt.io/qtforpython/
- Python CSV module: https://docs.python.org/3/library/csv.html
- Stack Overflow guidance on widget connections and exception handling
"""

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget
import csv
import os

class BudgetApp(QWidget):
    """
    A PyQt6 GUI application for managing a budget by tracking income and expenses.
    """

    def __init__(self):
        """
        Initialize the BudgetApp, load the UI, and connect buttons to their handlers.
        """
        super().__init__()
        uic.loadUi("budget.ui", self)
        self.setFixedSize(self.size())

        self.budget = 0.0
        self.total_expenses = 0.0
        self.total_income = 0.0

        self.addBudgetButton.clicked.connect(self.set_budget)
        self.addButton.clicked.connect(self.add_transaction)
        self.exitButton.clicked.connect(self.close)

        self.update_remaining()

    def set_budget(self):
        """
        Sets the user's budget from the input field.
        Validates that it is a positive number with max two decimal places.
        """
        try:
            value = float(self.budgetInput.text().strip())
            if value < 0 or round(value, 2) != value:
                raise ValueError
            self.budget = value
            self.budgetLabel.setText(f"Budget: ${self.budget:.2f}")
            self.resultLabel.setText("Budget set successfully.")
            self.resultLabel.setStyleSheet("color: green;")
            self.update_remaining()
        except ValueError:
            self.resultLabel.setText("Please enter a valid amount (max 2 decimal places).")
            self.resultLabel.setStyleSheet("color: red;")


    def add_transaction(self):
        """
        Adds a transaction (income or expense) based on user input.
        Validates amount and ensures two decimal precision.
        """
        amount_text = self.amountInput.text().strip()
        trans_type = self.transactionTypeDropdown.currentText()
        category = self.categoryDropdown.currentText()

        try:
            amount = float(amount_text)

            # Check for negative/zero values or more than 2 decimal places
            if amount <= 0 or round(amount, 2) != amount:
                raise ValueError

            if trans_type == "Expense":
                self.total_expenses += amount
            elif trans_type == "Income":
                self.total_income += amount

            self.resultLabel.setText(f"{trans_type} of ${amount:.2f} added.")
            self.resultLabel.setStyleSheet("color: green;")
            self.update_remaining()
            self.log_transaction(trans_type, amount, category)

        except ValueError:
            self.resultLabel.setText("Enter a valid amount (max 2 decimal places).")
            self.resultLabel.setStyleSheet("color: red;")


    def update_remaining(self):
        """
        Recalculates and displays the remaining budget.
        """
        remaining = self.budget + self.total_income - self.total_expenses
        self.remainingLabel.setText(f"Remaining: ${remaining:.2f}")

    def log_transaction(self, trans_type: str, amount: float, category: str):
        """
        Logs a transaction to a CSV file including type, amount, category, and current remaining budget.
        Creates the file if it doesn't exist.

        Args:
            trans_type (str): 'Income' or 'Expense'
            amount (float): The transaction amount
            category (str): The category selected by the user
        """
        os.makedirs("data", exist_ok=True)
        filename = "data/transactions.csv"
        file_exists = os.path.isfile(filename)
        remaining = self.budget + self.total_income - self.total_expenses

        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Type", "Amount", "Category", "Remaining"])
            writer.writerow([trans_type, f"{amount:.2f}", category, f"{remaining:.2f}"])
