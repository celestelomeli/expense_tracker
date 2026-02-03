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

-- Budget table to store monthly budget limit
CREATE TABLE IF NOT EXISTS budget (
    id INT AUTO_INCREMENT PRIMARY KEY,
    amount DECIMAL(10, 2) NOT NULL,     -- Monthly budget amount
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert budget of $500
INSERT INTO budget (amount) VALUES (500.00);

-- Sample expenses for demo
INSERT INTO expenses (date, category, amount, description) VALUES
('2026-02-01', 'Food', 45.50, 'Groceries'),
('2026-02-01', 'Transport', 15.00, 'Uber to work'),
('2026-02-02', 'Bills', 120.00, 'Internet bill'),
('2026-02-02', 'Entertainment', 50.00, 'Movie tickets'),
('2026-02-03', 'Healthcare', 35.00, 'Pharmacy'),
('2026-02-03', 'Food', 22.75, 'Lunch'),
('2026-02-04', 'Shopping', 85.00, 'Clothes'),
('2026-02-04', 'Transport', 12.50, 'Gas'),
('2026-02-05', 'Food', 18.25, 'Coffee'),
('2026-02-05', 'Other', 25.00, 'Gift');
