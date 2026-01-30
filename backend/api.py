# FastAPI Backend for Expense Tracker
# Converts CLI app to REST API for React frontend

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime, date

# Load environment variables from .env file
load_dotenv()

# Create FastAPI application instance
app = FastAPI(title="Expense Tracker API")

# Configure CORS to allow React (localhost:5173) to make requests to this API (localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, DELETE, )
    allow_headers=["*"],  # Allow all headers
)

# Pydantic models define the structure of request/response data
# FastAPI uses these for automatic validation and documentation

class ExpenseCreate(BaseModel):
    """Data structure for creating a new expense (from React form)"""
    date: str
    category: str
    amount: float
    description: str

class Expense(BaseModel):
    """Data structure for expense response (to React)"""
    id: int
    date: str
    category: str
    amount: float
    description: str

def get_db_connection():
    """
    Establish connection to MySQL database.
    Uses environment variables for credentials.
    Returns connection object or None if failed.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),        # Database server 
            user=os.getenv("DB_USER"),        
            password=os.getenv("DB_PASSWORD"), 
            database=os.getenv("DB_NAME")     
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}") # Log error to console
        return None

def validate_date(date_string: str) -> bool:
    """
    Validate date is in YYYY-MM-DD format.
    Returns True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_amount(amount: float) -> bool:
    """
    Validate amount is a positive number.
    Returns True if valid, False otherwise.
    """
    return amount > 0

# Predefined expense categories
CATEGORIES = ["Food", "Transport", "Bills", "Entertainment", "Shopping", "Healthcare", "Other"]

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/api/expenses")
def get_expenses():
    """
    GET /api/expenses
    Retrieve all expenses from database.
    Returns JSON with list of expenses.
    """
    # Connect to database
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Cursor to execute queries
    cursor = db.cursor()
    
    try:
        # Query all expenses, ordered by date (newest first)
        cursor.execute(
            "SELECT id, date, category, amount, description FROM expenses ORDER BY date DESC"
        )
        expenses = cursor.fetchall()
        
        # Convert database tuples to JSON-friendly dictionaries
        result = []
        for expense_id, exp_date, category, amount, description in expenses:
            result.append({
                "id": expense_id,
                "date": str(exp_date),      # Convert date object to string
                "category": category,
                "amount": float(amount),    # Ensure amount is float
                "description": description
            })
        
        # Return as JSON
        return {"expenses": result}
        
    except mysql.connector.Error as err:
        # If database error, return 500 error to React
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        # Always close cursor and connection
        cursor.close()
        db.close()

@app.post("/api/expenses")
def create_expense(expense: ExpenseCreate):
    """
    POST /api/expenses
    Create a new expense in database.
    Expects JSON body with date, category, amount, description.
    Returns success message with new expense ID.
    """
    # Validate date format
    if not validate_date(expense.date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    # Validate amount = positive
    if not validate_amount(expense.amount):
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    # Validate category is in predeinfined list
    if expense.category not in CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid category. Must be one of: {CATEGORIES}")
    
    # Connect to database
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = db.cursor()
    
    try:
        # Insert new expense into database
        sql = "INSERT INTO expenses (date, category, amount, description) VALUES (%s, %s, %s, %s)"
        values = (expense.date, expense.category, expense.amount, expense.description)
        
        cursor.execute(sql, values)
        db.commit()  # Save changes to database
        
        # Get the ID of the newly created expense
        expense_id = cursor.lastrowid
        
        # Return success message with ID
        return {
            "message": "Expense added successfully!",
            "id": expense_id
        }
        
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        db.close()

@app.delete("/api/expenses/{expense_id}")
def delete_expense(expense_id: int):
    """
    DELETE /api/expenses/{id}
    Delete an expense by ID.
    FastAPI extracts {expense_id} from URL path.
    Returns success message or 404 if not found.
    """
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = db.cursor()
    
    try:
        # Delete expense with matching ID
        cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
        
        # Check if any row was deleted
        if cursor.rowcount == 0:
            # No expense found with that ID
            raise HTTPException(status_code=404, detail=f"Expense with ID {expense_id} not found")
        
        db.commit()  # Save changes
        
        return {"message": f"Expense ID {expense_id} deleted successfully!"}
        
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        db.close()

@app.get("/api/summaries")
def get_summaries():
    """
    GET /api/summaries
    Get total spending grouped by date.
    Returns JSON with date and total for each day.
    """
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = db.cursor()
    
    try:
        # Query to sum amounts by date
        # GROUP BY groups expenses by date
        cursor.execute(
            "SELECT DATE_FORMAT(date, '%Y-%m-%d'), SUM(amount) "
            "FROM expenses GROUP BY DATE_FORMAT(date, '%Y-%m-%d') ORDER BY date DESC"
        )
        summaries = cursor.fetchall()
        
        # Convert to JSON format
        result = []
        for exp_date, total_amount in summaries:
            result.append({
                "date": exp_date,
                "total": float(total_amount)
            })
        
        return {"summaries": result}
        
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        db.close()

@app.get("/api/insights")
def get_insights():
    """
    GET /api/insights
    Calculate spending insights:
    - Average spending per expense
    - Highest single expense
    - Most frequently used category
    Returns JSON with all insights.
    """
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = db.cursor()
    
    try:
        # First check if there are any expenses
        cursor.execute("SELECT COUNT(*) FROM expenses")
        count = cursor.fetchone()[0]
        
        # If no expenses, return 0
        if count == 0:
            return {
                "average_spending": 0,
                "highest_expense": 0,
                "most_common_category": None,
                "category_count": 0
            }
        
        # Calculate average spending across all expenses
        cursor.execute("SELECT AVG(amount) FROM expenses")
        average_spending = cursor.fetchone()[0]
        
        # Find highest single expense
        cursor.execute("SELECT MAX(amount) FROM expenses")
        highest_expense = cursor.fetchone()[0]
        
        # Find most common category
        cursor.execute(
            "SELECT category, COUNT(*) as count FROM expenses "
            "GROUP BY category ORDER BY count DESC LIMIT 1"
        )
        result = cursor.fetchone()
        most_common_category = result[0]
        category_count = result[1]
        
        return {
            "average_spending": float(average_spending),
            "highest_expense": float(highest_expense),
            "most_common_category": most_common_category,
            "category_count": category_count
        }
        
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        db.close()

@app.get("/api/categories")
def get_categories():
    """
    GET /api/categories
    Return list of valid expense categories.
    Used by React to populate dropdown menu.
    """
    return {"categories": CATEGORIES}

@app.get("/")
def root():
    """
    GET /
    Root endpoint to verify API is running.
    Visit http://localhost:8000 to see this message.
    Visit http://localhost:8000/docs for interactive API documentation.
    """
    return {
        "message": "Expense Tracker API is running!",
        "docs": "Visit /docs for interactive API documentation"
    }
