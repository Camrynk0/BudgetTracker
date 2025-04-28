import sys
from PyQt6.QtWidgets import QApplication
from gui import BudgetApp

def main() -> None:
    """
    Launches the Budget Tracker application.
    """
    app = QApplication(sys.argv)
    window = BudgetApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
