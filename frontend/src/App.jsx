import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

// Base URL for FastAPI backend
const API_URL = 'http://localhost:8000/api'

function App() {
  // useState creates reactive variables - when they change, UI updates automatically
  const [expenses, setExpenses] = useState([])  // List of all expenses
  const [date, setDate] = useState('')  // Form input: date
  const [category, setCategory] = useState('Food')  // Form input: category
  const [amount, setAmount] = useState('')  // Form input: amount
  const [description, setDescription] = useState('')  // Form input: description
  const [categories, setCategories] = useState([])  // Valid categories from backend
  const [insights, setInsights] = useState(null)  // Analytics data

  // useEffect runs when component first loads 
  // Empty [] means "run once on load, never again"
  useEffect(() => {
    fetchExpenses()
    fetchCategories()
    fetchInsights()
  }, [])

  // Fetch all expenses from backend
  const fetchExpenses = async () => {
    try {
      const response = await axios.get(`${API_URL}/expenses`)  // GET request
      setExpenses(response.data.expenses)  // Update state with response; just array not wrapper object
    } catch (error) {
      console.error('Error fetching expenses:', error)
    }
  }

  // Fetch valid categories from backend
  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API_URL}/categories`)
      setCategories(response.data.categories)
    } catch (error) {
      console.error('Error fetching categories:', error)
    }
  }

  // Fetch insights (average, highest, most common)
  const fetchInsights = async () => {
    try {
      const response = await axios.get(`${API_URL}/insights`)
      setInsights(response.data)
    } catch (error) {
      console.error('Error fetching insights:', error)
    }
  }

  // Handle form submission when user clicks "Add Expense"
  const handleSubmit = async (e) => {
     // e = event object passed automatically by browser
    e.preventDefault()  // Prevent page reload on form submit to send data via axios
    
    try {
      // Send POST request with form data
      await axios.post(`${API_URL}/expenses`, {
        date,
        category,
        amount: parseFloat(amount),  // Convert string to number
        description
      })
      
      // Clear form inputs after successful submission to reset form
      setDate('')
      setAmount('')
      setDescription('')
      
      // Refresh data from backend
      fetchExpenses()
      fetchInsights()
      
      alert('Expense added successfully!')
    } catch (error) {
      alert('Error adding expense: ' + error.response?.data?.detail)
    }
  }

  // Delete expense by ID
  const handleDelete = async (id) => {
    if (!confirm('Delete this expense?')) return  // Confirm before deleting
    
    try {
      await axios.delete(`${API_URL}/expenses/${id}`)  // DELETE request
      fetchExpenses()  // Refresh list
      fetchInsights()  // Refresh analytics
      alert('Expense deleted!')
    } catch (error) {
      alert('Error deleting expense')
    }
  }

  // JSX Javacript XML: HTML-like syntax inside JavaScript; React converts to actual HTML
  return (
    <div className="app">
      <h1> Expense Tracker</h1>
      
      {/* Form Section */}
      <div className="form-container">
        <h2>Add Expense</h2>
        <form onSubmit={handleSubmit}>
          {/* Date input - value and onChange create two-way binding */}
          <input
            type="date"
            value={date}  // Controlled input: value comes from state
            onChange={(e) => setDate(e.target.value)}  // Update state on change
            required
          />
          
          {/* Category dropdown - populated from backend */}
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
          >
            {/* Loop through categories array and create <option> for each */}
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
          
          {/* Amount input - step="0.01" allows decimals */}
          <input
            type="number"
            step="0.01"
            placeholder="25.50"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
          />
          
          {/* Description input */}
          <input
            type="text"
            placeholder="e.g. Lunch at cafe"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
          
          <button type="submit">Add Expense</button>
        </form>
      </div>

      {/* Insights Section - only show if insights data exists */}
      {insights && (
        <div className="insights">
          <h2>Insights</h2>
          <p>Average: ${insights.average_spending.toFixed(2)}</p>
          <p>Highest: ${insights.highest_expense.toFixed(2)}</p>
          <p>Most Common: {insights.most_common_category} ({insights.category_count}x)</p>
        </div>
      )}

      {/* Expenses List Section */}
      <div className="expenses-list">
        <h2>Expenses</h2>
        {/* Conditional rendering: show message if empty, table if has data */}
        {expenses.length === 0 ? (
          <p>No expenses yet</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Category</th>
                <th>Amount</th>
                <th>Description</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {/* Loop through expenses and create table row for each */}
              {expenses.map(expense => (
                <tr key={expense.id}>  {/* key helps React track which items changed */}
                  <td>{expense.date}</td>
                  <td>{expense.category}</td>
                  <td>${expense.amount.toFixed(2)}</td>  {/* Format to 2 decimals */}
                  <td>{expense.description}</td>
                  <td>
                    {/* onClick passes expense.id to handleDelete */}
                    <button onClick={() => handleDelete(expense.id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default App
