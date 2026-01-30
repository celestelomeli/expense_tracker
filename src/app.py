import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Predefined expense categories
CATEGORIES = ["Food", "Transport", "Bills", "Entertainment", "Shopping", "Healthcare", "Other"]

def get_db_connection():
    """Create and return a database connection."""
    try:
        # Attempt to connect to MySQL using credentials from .env file
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),        # Database server address
            user=os.getenv("DB_USER"),        # Database username
            password=os.getenv("DB_PASSWORD"), # Database password
            database=os.getenv("DB_NAME")     # Database name to use
        )
        return connection
    except mysql.connector.Error as err:
        # If connection fails, print error and return None
        print(f"Error connecting to database: {err}")
        return None

def validate_date(date_string):
    """Validate date format (YYYY-MM-DD)."""
    try:
        # Try to parse the string as a date in YYYY-MM-DD format
        # If it fails, strptime will raise a ValueError
        datetime.strptime(date_string, '%Y-%m-%d')
        return True  # Date is valid
    except ValueError:
        return False  # Date is invalid

def validate_amount(amount_string):
    """Validate amount is a positive number."""
    try:
        # Try to convert string to float
        amount = float(amount_string)
        # Check if the amount is greater than 0
        return amount > 0
    except ValueError:
        # If conversion fails (not a number), return False
        return False

def select_category():
    """Display categories and let user select one."""
    print("\nCategories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}. {cat}")
    
    choice = input("Select (1-7): ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
        return CATEGORIES[int(choice) - 1]
    
    return None

def add_expense(cursor, db, date, category, amount, description):
    """Add a new expense to the database."""
    try:
        # SQL query with placeholders (%s) to prevent SQL injection
        sql = "INSERT INTO expenses (date, category, amount, description) VALUES (%s, %s, %s, %s)"
        values = (date, category, amount, description)
        
        # Execute the query with the provided values
        cursor.execute(sql, values)
        
        # Commit the changes to the database
        db.commit()
        
        print("\n[SUCCESS] Expense added successfully!")
    except mysql.connector.Error as err:
        # If database operation fails, print the error
        print(f"\n[ERROR] Error adding expense: {err}")

def view_summaries(cursor):
    """Display expense summaries grouped by date."""
    try:
        # Query to get total spending per date, sorted newest first
        # DATE_FORMAT formats the date, SUM adds up all amounts for that date
        cursor.execute("SELECT DATE_FORMAT(date, '%Y-%m-%d'), SUM(amount) FROM expenses GROUP BY DATE_FORMAT(date, '%Y-%m-%d') ORDER BY date DESC")
        
        # Fetch all results as a list of tuples
        summaries = cursor.fetchall()
        
        # Check if there are any expenses
        if not summaries:
            print("\nNo expenses found.")
            return
        
        print("\n=== Expense Summaries ===")
        # Loop through each date and its total
        for date, total_amount in summaries:
            # Format and print each summary line
            print(f"{date}: ${total_amount:.2f}")
    except mysql.connector.Error as err:
        print(f"\n[ERROR] Error fetching summaries: {err}")

def generate_insights(cursor):
    """Generate and display spending insights."""
    try:
        # Check if there are any expenses
        cursor.execute("SELECT COUNT(*) FROM expenses")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("\nNo expenses found. Add some expenses first!")
            return
        
        # Calculate average spending
        cursor.execute("SELECT AVG(amount) FROM expenses")
        average_spending = cursor.fetchone()[0]
        
        # Get highest expense
        cursor.execute("SELECT MAX(amount) FROM expenses")
        highest_expense = cursor.fetchone()[0]
        
        # Get most common category
        cursor.execute("SELECT category, COUNT(*) as count FROM expenses GROUP BY category ORDER BY count DESC LIMIT 1")
        most_common_category = cursor.fetchone()
        
        print("\n=== Expense Insights ===")
        print(f"Average Spending: ${average_spending:.2f}")
        print(f"Highest Expense: ${highest_expense:.2f}")
        print(f"Most Common Category: {most_common_category[0]} ({most_common_category[1]} expenses)")
    except mysql.connector.Error as err:
        print(f"\n[ERROR] Error generating insights: {err}")

def delete_expense(cursor, db):
    """Delete an expense by ID."""
    try:
        # Show all expenses with IDs so user can choose which to delete
        cursor.execute("SELECT id, date, category, amount, description FROM expenses ORDER BY date DESC")
        expenses = cursor.fetchall()
        
        # Check if there are any expenses to delete
        if not expenses:
            print("\nNo expenses to delete.")
            return
        
        print("\n=== All Expenses ===")
        # Display each expense with its ID
        for expense_id, date, category, amount, description in expenses:
            print(f"ID {expense_id}: {date} | {category} | ${amount:.2f} | {description}")
        
        # Get user input for which expense to delete
        expense_id = input("\nEnter expense ID to delete (or 'c' to cancel): ")
        
        # Allow user to cancel the delete operation
        if expense_id.lower() == 'c':
            print("Delete cancelled.")
            return
        
        # Validate that input is a number
        if not expense_id.isdigit():
            print("\n[ERROR] Invalid ID. Please enter a number.")
            return
        
        # Execute delete query with the provided ID
        cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
        
        # Check if any row was actually deleted
        if cursor.rowcount > 0:
            # Save the deletion to database
            db.commit()
            print(f"\n[SUCCESS] Expense ID {expense_id} deleted successfully!")
        else:
            # No expense found with that ID
            print(f"\n[ERROR] No expense found with ID {expense_id}.")
    except mysql.connector.Error as err:
        print(f"\n[ERROR] Error deleting expense: {err}")

def filter_by_date_range(cursor):
    """Display expenses within a date range."""
    try:
        # Get start date from user
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        if not validate_date(start_date):
            print("\n[ERROR] Invalid start date format.")
            return
        
        # Get end date from user
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        if not validate_date(end_date):
            print("\n[ERROR] Invalid end date format.")
            return
        
        # Query expenses between the two dates
        cursor.execute(
            "SELECT date, category, amount, description FROM expenses "
            "WHERE date BETWEEN %s AND %s ORDER BY date DESC",
            (start_date, end_date)
        )
        expenses = cursor.fetchall()
        
        # Check if any expenses found
        if not expenses:
            print(f"\nNo expenses found between {start_date} and {end_date}.")
            return
        
        # Display results
        print(f"\n=== Expenses from {start_date} to {end_date} ===")
        total = 0
        for date, category, amount, description in expenses:
            print(f"{date} | {category} | ${amount:.2f} | {description}")
            total += amount
        print(f"\nTotal: ${total:.2f}")
        
    except mysql.connector.Error as err:
        print(f"\n[ERROR] Error filtering by date: {err}")

def filter_by_category(cursor):
    """Display all expenses for a specific category."""
    try:
        # Get category from predefined list
        category = select_category()
        if not category:
            print("\n[ERROR] Invalid category.")
            return
        
        # Query expenses for that category
        cursor.execute(
            "SELECT date, amount, description FROM expenses "
            "WHERE category = %s ORDER BY date DESC",
            (category,)
        )
        expenses = cursor.fetchall()
        
        # Check if any expenses found
        if not expenses:
            print(f"\nNo expenses found for category '{category}'.")
            return
        
        # Display results
        print(f"\n=== Expenses for '{category}' ===")
        total = 0
        for date, amount, description in expenses:
            print(f"{date} | ${amount:.2f} | {description}")
            total += amount
        print(f"\nTotal: ${total:.2f}")
        
    except mysql.connector.Error as err:
        print(f"\n[ERROR] Error filtering by category: {err}")

def main():
    """Main function to run the expense tracker application."""
    # Establish database connection
    db = get_db_connection()
    if not db:
        print("Failed to connect to database. Exiting.")
        return
    
    # Create cursor object to execute SQL queries
    cursor = db.cursor()
    
    try:
        # Main application loop: runs until user chooses to exit
        while True:
            # Display menu
            print("\n" + "="*30)
            print("    EXPENSE TRACKER")
            print("="*30)
            print("1. Add Expense")
            print("2. View Summaries")
            print("3. Generate Insights")
            print("4. Delete Expense")
            print("5. Filter by Date Range")
            print("6. Filter by Category")
            print("7. Exit")
            print("="*30)
            
            # Get user's menu choice and remove any extra whitespace
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == "1":
                # Add expense with validation
                date = input("Enter date (YYYY-MM-DD): ").strip()
                if not validate_date(date):
                    print("\n[ERROR] Invalid date format. Please use YYYY-MM-DD.")
                    continue  # Skip rest of loop and show menu again
                
                # Select category from predefined list
                category = select_category()
                if not category:
                    print("\n[ERROR] Invalid category.")
                    continue
                
                amount_input = input("Enter amount: ").strip()
                if not validate_amount(amount_input):
                    print("\n[ERROR] Invalid amount. Please enter a positive number.")
                    continue
                
                # Convert validated amount to float
                amount = float(amount_input)
                description = input("Enter description: ").strip()
                
                # Call function to add expense to database
                add_expense(cursor, db, date, category, amount, description)
                
            elif choice == "2":
                # Display expense summaries
                view_summaries(cursor)
                
            elif choice == "3":
                # Display spending insights
                generate_insights(cursor)
                
            elif choice == "4":
                # Delete an expense
                delete_expense(cursor, db)
                
            elif choice == "5":
                # Filter by date range
                filter_by_date_range(cursor)
                
            elif choice == "6":
                # Filter by category
                filter_by_category(cursor)
                
            elif choice == "7":
                # Exit the application
                print("\nThank you for using Expense Tracker. Goodbye!")
                break  # Exit the while loop
                
            else:
                # Handle invalid menu choices
                print("\n[ERROR] Invalid choice. Please enter a number between 1 and 7.")
    
    finally:
        # block always runs, even if there's an error
        # Always close database connections to free up resources
        cursor.close()
        db.close()

if __name__ == "__main__":
    main()
