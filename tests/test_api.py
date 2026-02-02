"""  
Unit tests for the Expense Tracker API

This file tests the FastAPI endpoints to ensure they work correctly.

Note: Run 'make start' before running tests to start the database.
"""

import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv
import sys
import os

# Load test environment variables from .env.test
load_dotenv('.env.test')

# Tells python where to find the api.py file
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import the FastAPI app from api.py
from api import app

# Create a test client 
client = TestClient(app)


def test_get_categories():
    """
    Test that we can get the list of expense categories.
    
    """
    # Act - Make a GET request to /api/categories
    response = client.get("/api/categories")
    
    # Print response for debugging (use -s flag to see this)
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Assert - Check if it worked
    assert response.status_code == 200  # 200 = success
    
    # Check for expected categories
    data = response.json()
    categories = data["categories"]
    
    # Check for all 7 categories
    expected = ["Food", "Transport", "Bills", "Entertainment", 
                "Shopping", "Healthcare", "Other"]
    assert categories == expected


def test_create_expense():
    """
    Test that we can add a new expense.
    """
    # Arrange - Create test expense data
    expense_data = {
        "date": "2026-02-02",
        "category": "Food",
        "amount": 25.50,
        "description": "Test lunch"
    }
    
    # Act - Send POST request to create expense
    response = client.post("/api/expenses", json=expense_data)
    
    # Print for debugging
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Assert - Check if it was created successfully
    assert response.status_code == 201  # 201 = created
    data = response.json()
    assert "Expense added" in data["message"]
    assert "id" in data  # Should return the new expense ID


def test_get_expenses():
    """
    Test that we can retrieve all expenses.
    """
    # Act - Get all expenses
    response = client.get("/api/expenses")
    
    # Print for debugging
    print(f"\nStatus: {response.status_code}")
    print(f"Number of expenses: {len(response.json()['expenses'])}")
    
    # Assert - Check if request was successful
    assert response.status_code == 200
    data = response.json()
    assert "expenses" in data  # Response should have an "expenses" key
    assert isinstance(data["expenses"], list)  # Should be a list


def test_delete_expense():
    """
    Test that we can delete an expense.
    
    Test first creates an expense, then deletes it.
    """
    # Arrange - First create an expense to delete
    expense_data = {
        "date": "2026-02-02",
        "category": "Transport",
        "amount": 10.00,
        "description": "Test expense to delete"
    }
    create_response = client.post("/api/expenses", json=expense_data)
    expense_id = create_response.json()["id"]
    
    # Act - Delete the expense
    response = client.delete(f"/api/expenses/{expense_id}")
    
    # Print for debugging
    print(f"\nDeleted expense ID: {expense_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Assert - Check if deletion was successful
    assert response.status_code == 200
    data = response.json()
    assert "deleted" in data["message"].lower()


# Run all tests:
# pytest tests/test_api.py -v
