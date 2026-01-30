import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Establish a connection to the database
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Create cursor to interact with the database
cursor = db.cursor()

# Add expense 
def add_expense(date, category, amount, description):
    # Insert data into expenses table 
    sql = "INSERT INTO expenses (date, category, amount, description) VALUES (%s, %s, %s, %s)"
    values = (date, category, amount, description)
    # Execute SQL query with provided values
    cursor.execute(sql, values)
    # Save changes permanently to database
    db.commit()

# View expense summaries
# Processes each row in table, formats the date column and groups results by formatted date
def view_summaries():
    cursor.execute("SELECT DATE_FORMAT(date, '%Y-%m-%d'), SUM(amount) FROM expenses GROUP BY DATE_FORMAT(date, '%Y-%m-%d')")
    # Results are fetched and stored in summaries variable
    # tuples containing date and total amount spent for that date
    summaries = cursor.fetchall()

    print("\nExpense Summaries:")
    #loop that iterates over each tuple in summaries list
    for date, total_amount in summaries:
        #prints each summary in specified format
        print(f"{date}: Total amount spent - ${total_amount:.2f}")


# Generate insights
def generate_insights():
    # Sql query calculates the average(AVG) of the amount column from expenses table
    cursor.execute("SELECT AVG(amount) FROM expenses")
    # Calculated average is then assigned to the variable average_spending
    average_spending = cursor.fetchone()[0]
    # Retrieves the maximum value from "amount" column in expenses table
    cursor.execute("SELECT MAX(amount) FROM expenses")
    # Max value assigned to highest_expense
    highest_expense = cursor.fetchone()[0]
    # Select two columns: "category" and the count of occurrences of each category in table
    # "LIMIT 1" part ensures that only the top result(most common category) is retrieved
    cursor.execute("SELECT category, COUNT(*) as count FROM expenses GROUP BY category ORDER BY count DESC LIMIT 1")
    # fetchone() method is tuple containing "Category" and "count" values for most common category
    most_common_category = cursor.fetchone()

    print("\nExpense Insights:")
    print(f"Average Spending: ${average_spending:.2f}")
    print(f"Highest Expense: ${highest_expense:.2f}")
    #most_common_category[0] and [1] placeholders get replaced with the values of the respective 
    #elements in the most_common_category tuple
    print(f"Most Common Category: {most_common_category[0]} (Count: {most_common_category[1]})")

#main function that handles user interaction, input, and menu options for tracker
def main():
    while True:
        #display the main menu options
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Summaries")
        print("3. Generate Insights")
        print("4. Exit")

        #Get user's choice from menu
        choice = input("Enter your choice: ")

        #Handle the user's choice
        if choice == "1":
            #Get input for adding an expense
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            description = input("Enter description: ")
            #call the add_expense function to add the expense to the database
            add_expense(date, category, amount, description)
            print("Expense added successfully!")
        elif choice == "2":
            #call the view_summaries function to display expense summaries
            view_summaries()
        elif choice == "3":
            #call the generate_insights function to display insights
            generate_insights()
        elif choice == "4":
            # Exit the program
            break
        else:
            # Invalid choice handling
            print("Invalid choice")

    # Close the cursor and the database connection when complete
    cursor.close()
    db.close()

#check if the script is being run as the main program 
if __name__ == "__main__":
    main()
