from PyQt6 import uic
from PyQt6.QtWidgets import QWidget
import csv
import os

class BudgetApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("budget.ui", self)
        self.setFixedSize(self.size())

        # Budget tracking
        self.budget = 0.0
        self.total_expenses = 0.0
        self.total_income = 0.0

        # Button connections
        self.addBudgetButton.clicked.connect(self.set_budget)
        self.addButton.clicked.connect(self.add_transaction)
        self.exitButton.clicked.connect(self.close)

        self.update_remaining()

    def set_budget(self):
        """
        Set the budget from the input field and update display.
        """
        try:
            value = float(self.budgetInput.text().strip())
            if value < 0:
                raise ValueError
            self.budget = value
            self.budgetLabel.setText(f"Budget: ${self.budget:.2f}")
            self.resultLabel.setText("Budget set successfully.")
            self.resultLabel.setStyleSheet("color: green;")
            self.update_remaining()
        except ValueError:
            self.resultLabel.setText("Please enter a valid positive number.")
            self.resultLabel.setStyleSheet("color: red;")

    def add_transaction(self):
        """
        Add an income or expense and update the remaining budget.
        """
        amount_text = self.amountInput.text().strip()
        trans_type = self.transactionTypeDropdown.currentText()
        category = self.categoryDropdown.currentText()

        try:
            amount = float(amount_text)
            if amount <= 0:
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
            self.resultLabel.setText("Enter a valid amount.")
            self.resultLabel.setStyleSheet("color: red;")

    def update_remaining(self):
        """
        Calculate and show remaining budget.
        """
        remaining = self.budget + self.total_income - self.total_expenses
        self.remainingLabel.setText(f"Remaining: ${remaining:.2f}")

    def log_transaction(self, trans_type: str, amount: float, category: str):
        os.makedirs("data", exist_ok=True)
        filename = "data/transactions.csv"
        file_exists = os.path.isfile(filename)

        # Calculate current remaining total
        remaining = self.budget + self.total_income - self.total_expenses

        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Type", "Amount", "Category", "Remaining"])
            writer.writerow([trans_type, f"{amount:.2f}", category, f"{remaining:.2f}"])

