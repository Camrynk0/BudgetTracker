from PyQt6 import uic
from PyQt6.QtWidgets import QWidget
import csv
import os

class BudgetApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("budget.ui", self)
        self.setFixedSize(self.size())  # Lock window size

        # Track budget and totals
        self.budget = 0.0
        self.total_expenses = 0.0
        self.total_income = 0.0

        # Connect GUI elements to methods
        self.addButton.clicked.connect(self.add_transaction)
        self.budgetInput.returnPressed.connect(self.set_budget)

        self.update_remaining()

    def set_budget(self):
        """Set the user's total budget from the input field."""
        try:
            value = float(self.budgetInput.text().strip())
            if value < 0:
                raise ValueError
            self.budget = value
            self.update_remaining()
            self.resultLabel.setText(f"Budget set to ${self.budget:.2f}")
            self.resultLabel.setStyleSheet("color: green;")
        except ValueError:
            self.resultLabel.setText("Error: Invalid budget amount.")
            self.resultLabel.setStyleSheet("color: red;")

    def update_remaining(self):
        """Update the remaining budget label based on current totals."""
        balance = self.budget - self.total_expenses
        self.remainingLabel.setText(f"Remaining: ${balance:.2f}")

    def add_transaction(self):
        """Add a transaction and update totals and CSV."""
        category = self.categoryDropdown.currentText()
        description = self.descriptionInput.text().strip()
        amount_text = self.amountInput.text().strip()
        trans_type = self.typeDropdown.currentText()

        # Validate fields
        if not description or not amount_text:
            self.resultLabel.setText("Error: All fields required!")
            self.resultLabel.setStyleSheet("color: red;")
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            self.resultLabel.setText("Error: Amount must be a positive number!")
            self.resultLabel.setStyleSheet("color: red;")
            return

        # Update totals
        if trans_type == "Expense":
            self.total_expenses += amount
        else:
            self.total_income += amount

        self.save_transaction(category, description, amount, trans_type)
        self.update_remaining()

        self.resultLabel.setText(f"{trans_type} added successfully.")
        self.resultLabel.setStyleSheet("color: green;")

    def save_transaction(self, category, description, amount, trans_type, filename="data/transactions.csv"):
        """Save transaction to CSV and include updated totals."""
        try:
            os.makedirs("data", exist_ok=True)
            rows = []
            file_exists = os.path.isfile(filename)

            # Load existing rows (excluding old totals)
            if file_exists:
                with open(filename, mode='r', newline='') as f:
                    reader = csv.reader(f)
                    rows = [row for row in reader if not row or not row[0].startswith("Totals")]

            # Re-write file with new transaction and updated totals
            with open(filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                if not file_exists or (rows and rows[0] != ["Category", "Description", "Amount", "Type"]):
                    writer.writerow(["Category", "Description", "Amount", "Type"])
                for row in rows[1:] if rows else []:
                    writer.writerow(row)
                writer.writerow([category, description, f"{amount:.2f}", trans_type])
                writer.writerow(["Totals", f"Income: {self.total_income:.2f}", f"Expenses: {self.total_expenses:.2f}",
                                 f"Balance: {self.total_income - self.total_expenses:.2f}"])
        except Exception as e:
            self.resultLabel.setText("Error saving transaction.")
            self.resultLabel.setStyleSheet("color: red;")
