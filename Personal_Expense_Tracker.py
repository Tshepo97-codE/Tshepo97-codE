# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os 
import csv
from collections import defaultdict
from datetime import datetime

file_name = "expenses.csv"

#intialization
def initialize_file():
    if not os.path.exists(file_name):
        with open(file_name, mode="w") as file:
            file.write("Date, Category, Amount\n")
        print(f"File '{file_name}' created successfully.")
    else:
        print(f"File '{file_name}' already exists.")

def add_expense():
    # Get user input
    date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
    date = date if date else datetime.now().strftime("%Y-%m-%d") # Default to today
    category = input("Enter category (e.g. food, Rent, Transport): ").strip().lower()
    amount = input("Enter amount: ").strip()
    
    # Validate the amount
    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    # Save to the file 
    with open(file_name, mode="a") as file:
        file.write(f"{date.strip()},{category.strip()},{amount:.2f}\n")
    print("Expense added successfully!")
        
# View all expenses
def view_expenses():
    try:
        with open(file_name, mode = "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            
            if len(rows) <= 1:
                print("\nNo expenses recorded yet.")
                return
            
            print("\n=== All expenses ===")
            for row in rows:
                print(f"{row[0]:<15} {row[1]:<15} {row[2]:<10}") # Format output
    except FileNotFoundError:
            print("\nNo expense file found. Please add an expense first.")

# Analyze spending
def analyze_spending():
    """Analyze spending by category."""
    try:
        with open(file_name, mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            
            if not rows:  # Check if only the header exists
                print("\nNo expenses recorded yet.")
                return

            total_spending = 0
            category_spending = defaultdict(float)

            for row in rows:  
                try:
                    # Normalize category and parse amount
                    category = row[1].strip().lower()  # Normalize category
                    amount = float(row[2].strip())     # Convert amount to float
                    total_spending += amount
                    category_spending[category] += amount
                except IndexError:
                    print(f"Skipping row: malformed line - {row}")
                except ValueError:
                    print(f"Skipping row: invalid amount - {row}")

            # Display results
            print("\n=== Spending Analysis ===")
            print(f"Total Spending: {total_spending:.2f}")
            print("\nSpending by Category:")
            for category, amount in category_spending.items():
                print(f"{category.capitalize()}: {amount:.2f}")
    except FileNotFoundError:
        print("\nNo expense file found. Please add an expense first.")

def clear_all_data(file_name = "expenses.csv"):
    """Clears all data from the expense file."""
    try: 
        with open(file_name, mode = "w") as file:
            file.write("Date,Category,Amount\n")
        print("All data has been cleared succesfully.")
    except FileNotFoundError:
            print("No expense file found to clear.")

def clear_category():
    """Clear data for a specific category."""
    try:
        category_to_clear = input("Enter the category to clear: ").strip().title()
        with open(file_name, mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        remaining_rows = [rows[0]]  # Keep the header row
        remaining_rows.extend(row for row in rows[1:] if row[1].title() != category_to_clear)

        with open(file_name, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(remaining_rows)

        print(f"Data for category '{category_to_clear}' has been cleared.")
    except FileNotFoundError:
        print("No expense file found to clear.")

def clear_analysis():
         """Clears analysis results (if stored in memory)."""
         global analysis_data
         analysis_data = [] # Reset analysis data
         print("Analysis data has been cleared.")

# Menu system
def display_menu():
    print("\n=== Personal Expense Tracker ===")
    print("1. Add an Expense") 
    print("2. View all Expenses")
    print("3. Analyze Spending")
    print("4. Clear All Data")
    print("5. Clear Specific Category")
    print("6. Clear Analysis Results")
    print("7. Exit")
    
#Main Program
def main():
    initialize_file()
    global analysis_data
    analysis_data = []
    
while True:
    display_menu()
    choice = input("Choose an option (1-7): ").strip()

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        analyze_spending()
    elif choice == "4":
        clear_all_data()
    elif choice == "5":
        clear_category()
    elif choice == "6":
        clear_analysis()
    elif choice == "7":
        print("Exiting program. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
