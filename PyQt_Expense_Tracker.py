
from PyQt5.QtWidgets import(QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QInputDialog) 
import sys 
import matplotlib.pyplot as plt 
import csv 
from collections import defaultdict 
from datetime import datetime

file_name = "expenses.csv" # Your expense file

class ExpenseTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Expense Tracker")
        self.setGeometry(200, 200, 400, 300)

        # Layout
        layout = QVBoxLayout()

        # Buttons
        self.add_button = QPushButton("Add Expense")
        self.view_button = QPushButton("View Expense")
        self.analyze_button = QPushButton("Analyze Spending")
        self.plot_button = QPushButton("Visualize Spending")

        # Add buttons to layout
        layout.addWidget(self.add_button)
        layout.addWidget(self.view_button)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.plot_button)

        # Connecct buttons to functions
        self.add_button.clicked.connect(self.add_expenses)
        self.view_button.clicked.connect(self.view_expenses)
        self.analyze_button.clicked.connect(self.analyze_spending)
        self.plot_button.clicked.connect(self.plot_spending)

        # Central Widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # New buttons for clearing data
        self.clear_all_button = QPushButton("Clear all Data")
        self.clear_all_button.clicked.connect(self.clear_all_data)
        layout.addWidget(self.clear_all_button)

        self.clear_category_button = QPushButton("Clear Specific Category")
        self.clear_category_button.clicked.connect(self.clear_category_input)
        layout.addWidget(self.clear_category_button)

    def add_expenses(self):
        """Add an expense to the file."""
        date, ok1 = QInputDialog.getText(self, "Add Expense", "Enter Date (YYYY-MM-DD):")
        if not ok1:
            QMessageBox.warning(self, "Error", "Invalid date entered.")
            return
        # Use today's date if input is empty
        date = date.strip() if date.strip() else datetime.now().strftime("%Y-%m-%d")

        category, ok2 = QInputDialog.getText(self, "Add Expense", "Enter the category:")
        if not ok2 or not category.strip():
            QMessageBox.warning(self, "Error", "Invalid category entered.")
            return

        amount, ok3 = QInputDialog.getDouble(self, "Add Expense", "Enter the amount:", 0, 0)
        if not ok3:
            QMessageBox.warning(self, "Error", "Invalid amount entered.")
            return

        try:
            with open(file_name, mode = "a", newline = "") as file:
                writer = csv.writer(file)
                writer.writerow([date.strip(), category.strip().title(), f"{amount:.2f}"])
            QMessageBox.information(self, "Success", "Expense added successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")


    def view_expenses(self):
        file_name = "expenses.csv"
        
        try:
            with open(file_name, mode = "r") as file: 
                expenses = file.readlines() 

            if not expenses:
                QMessageBox.information(self, "View Expenses", "No expenses recorded yet.")
                return

            # Organize and capitalize categories
            expense_summary = {}
            for line in expenses:
                date, category, amount = line.strip().split(",")
                category = category.title()  # Capitalize the first letter of each word
                amount = float(amount)

                if category in expense_summary:
                    expense_summary[category] += amount
                else:
                    expense_summary[category] = amount

            # Sort expenses by category
            sorted_expenses = sorted(expense_summary.items())

            # Create a neat display
            display_text = "Category\t\tAmount\n" + "-" * 30 + "\n"
            for category, amount in sorted_expenses:
                display_text += f"{date:<15} {category:<20} {amount:.2f}\n"

            QMessageBox.information(self, "View Expenses", display_text)

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No expense file found. Please add an expense first.")

    def analyze_spending(self):
        try:
            with open(file_name, mode="r") as file:
                reader = csv.reader(file)
                rows = list(reader)

                if not rows:
                    QMessageBox.information(self, "Info", "No expenses recorded yet.")
                    return

                total_spending = 0
                category_spending = defaultdict(float)

                for row in rows:
                    # Skip empty or malformed rows
                    if len(row) < 3 or not row[2].strip():
                        continue
                    category = row[1].strip().lower()
                    try:
                        amount = float(row[2])
                    except ValueError:
                        QMessageBox.warning(self, "Error", f"Invalid amount value in row: {row}")
                        continue
                    total_spending += amount
                    category_spending[category] += amount

                # Display results
                results = f"Total Spending: {total_spending:.2f}\nSpending by Category:\n"
                for category, amount in category_spending.items():
                    results += f"{category.title()}: {amount:.2f}\n"
                QMessageBox.information(self, "Spending Analysis", results)

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No expenses file found. Please add an expense first.")

    def plot_spending(self):
        try:
            with open(file_name, mode = "r") as file:
                reader = csv.reader(file)
                rows = list(reader)

                if not rows:
                    QMessageBox.information(self, "info", "No expenses recorded yet.")
                    return

                category_spending = defaultdict(float)
                for row in rows:
                    if len(row) == 3:
                        category = row[1]
                        amount = float(row[2])
                        category_spending[category] += amount 

                categories = list(category_spending.keys())
                amounts = list(category_spending.values())

                plt.bar(categories, amounts, color = 'skyblue')
                plt.xlabel("Categories")
                plt.ylabel("Spending (Amount)")
                plt.title("Spending by Category")
                plt.xticks(rotation = 45)
                plt.tight_layout()
                plt.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No expense file found. Please add an expense first.")

    # Function to clear all data
    def clear_all_data(self):
        """Clears all stored data from the expense file and resets analysis data"""
        file_name = "expenses.csv"
        try:
            # open the file in write mode to clear its contents
            with open(file_name, mode = "w") as file:
                pass # This clears the file

            # Reset in-memory analysis data
            self.analysis_data = []

            QMessageBox.information(self, "Success", "All data has been cleared successfully.")
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No expense file found to clear.")

    def clear_category(self, category_to_clear):
        """Clears all data for a specific category, and updates the spending analysis."""
        try:
            with open(file_name, mode="r") as file:
                rows = list(csv.reader(file))

            # Filter out rows that match the specified category
            remaining_rows = [
                row for row in rows if len(row) >= 3 and row[1].strip().lower() != category_to_clear.strip().lower()
            ]

            # Write the filtered data back to the file
            with open(file_name, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(remaining_rows)

            QMessageBox.information(self, "Success", f"Data for category '{category_to_clear}' has been cleared.")
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No expense file found to clear.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An unexpected error occurred: {e}")

    def clear_category_input(self):
        """Prompts the user for a category name to clear."""
        category, ok = QInputDialog.getText(self, "Clear Category", "Enter the category to clear:")
        if ok and category:
            self.clear_category(category)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTracker()
    window.show()
    sys.exit(app.exec_())