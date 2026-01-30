-- Database initialization script
-- Runs automatically when MySQL container starts for the first time
-- Creates the expenses table if it doesn't already exist

CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each expense, auto-increments 
    date DATE NOT NULL,                 -- Date of the expense 
    category VARCHAR(100) NOT NULL,     -- Category name 
    amount DECIMAL(10, 2) NOT NULL,     -- Dollar amount with 2 decimal places (25.50)
    description TEXT                    -- Optional description of the expense
);
