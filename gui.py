from PyQt6 import uic
from PyQt6.QtWidgets import QWidget

class BudgetApp(QWidget):
    """
    A simple budget tracker GUI for entering transactions.
    """

    def __init__(self):
        """
        Initialize the BudgetApp GUI and set up button connections.
        """
        super().__init__()
        uic.loadUi("budget.ui", self)

        self.setFixedSize(self.size())  # Lock window size

        # Connect the Add Transaction button
        self.addButton.clicked.connect(self.add_transaction)

    def add_transaction(self) -> None:
        """
        Validate the transaction fields and show success or error message.
        """
        category = self.categoryDropdown.currentText()
        description = self.descriptionInput.text().strip()
        amount_text = self.amountInput.text().strip()
        trans_type = self.typeDropdown.currentText()

        # Check if any field is empty
        if not category or not description or not amount_text:
            self.resultLabel.setText("Error: All fields required!")
            self.resultLabel.setStyleSheet("color: red;")
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                self.resultLabel.setText("Error: Amount must be greater than zero!")
                self.resultLabel.setStyleSheet("color: red;")
                return

            # All inputs are valid
            self.resultLabel.setText(f"Transaction added: {trans_type}")
            self.resultLabel.setStyleSheet("color: green;")

        except ValueError:
            self.resultLabel.setText("Error: Amount must be a valid number!")
            self.resultLabel.setStyleSheet("color: red;")
