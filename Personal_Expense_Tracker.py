# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os 
import csv

file_name = "expenses.csv"

#intialization

def initialize_file():
    if not os.path.exists(file_name):
        with open(file_name, mode="w") as file:
            file.write("Date, Category, Amount\n")
        print(f"File '{file_name}' created successfully.")
    else:
        print(f"File '{file_name}' already exists.")

from datetime import datetime

def add_expense():
    # Get user input
    date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
    date = date if date else datetime.now().strftime("%Y-%m-%d") # Default to today
    category = input("Enter category (e.g. food, Rent, Transport): ").strip()
    amount = input("Enter amount: ").strip()
    
    #Validate the amount
    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

# Save to the file 
    with open(file_name, mode = "a") as file:
        file.write(f"{date},{category},{amount}\n")
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

from collections import defaultdict

# Analyze spending
def analyze_spending():
    try:
        with open(file_name, mode = "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            
            if len(rows) <= 1: # Only if header exists
                print("\nNo expenses recorded yet.")
                return
            
            total_spending = 0
            category_spending = defaultdict(float)
            
            # Skip the header and process each row
            for row in rows[1:]:
                category = row[1]
                amount = float(row[2])
                total_spending += amount
                category_spending[category] += amount
                
            # Display results
            print("\n=== Spending Analysis ===")
            print(f"Total Spending: {total_spending:.2f}")
            print("\nSpending by Category: ")
            for category, amount in category_spending.items():
                print(f"{category}: {amount:.2f}")
    except FileNotFoundError:
            print("\nNo expense file found. Please add an expense first.")
            
# Menu system
def display_menu():
    print("\n=== Personal Expense Tracker ===")
    print("1. Add an Expense") 
    print("2. View all Expenses")
    print("3. Analyze Spending")
    print("4. Exit")
    
#Main Program
initialize_file()

while True:
    display_menu()
    choice = input("Choose an option (1-4): ")
    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        analyze_spending()
    elif choice == "4":
        print("Exiting program. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
        

        
