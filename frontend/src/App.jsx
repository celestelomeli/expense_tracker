import { useState, useEffect } from 'react'  // useState = manage state, useEffect = run code on load

// Axios - HTTP client for making API requests to backend
import axios from 'axios'

// Chart.js - charting library for data visualization
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js'
import { Pie } from 'react-chartjs-2'  // React wrapper for Chart.js pie charts
import './App.css'

// Register Chart.js components for charts to work
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement)

// Base URL for FastAPI backend
const API_URL = 'http://localhost:8000/api'

function App() {
  // useState creates reactive variables - when they change, UI updates automatically
  const [expenses, setExpenses] = useState([])  // List of all expenses
  const [date, setDate] = useState('')  // Form input: date
  const [category, setCategory] = useState('Food') 
  const [amount, setAmount] = useState('') 
  const [description, setDescription] = useState('') 
  const [categories, setCategories] = useState([]) 
  const [insights, setInsights] = useState(null) 
  const [monthlyBudget, setMonthlyBudget] = useState(500)  
  const [budgetInput, setBudgetInput] = useState('')  // Input field for changing budget

  // Empty [] means "only run once on load"
  useEffect(() => {
    fetchExpenses()
    fetchCategories()
    fetchInsights()
    fetchBudget()
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

  // Fetch budget from backend
  const fetchBudget = async () => {
    try {
      const response = await axios.get(`${API_URL}/budget`)
      setMonthlyBudget(response.data.budget)
    } catch (error) {
      console.error('Error fetching budget:', error)
    }
  }

  // Update budget
  const handleBudgetUpdate = async () => {
    const newBudget = parseFloat(budgetInput)
    
    if (!newBudget || newBudget <= 0) {
      alert('Please enter a valid budget amount')
      return
    }
    
    try {
      await axios.post(`${API_URL}/budget`, { amount: newBudget })
      setMonthlyBudget(newBudget)
      setBudgetInput('')
      alert('Budget updated successfully!')
    } catch (error) {
      alert('Error updating budget')
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

  // Prepare data for pie chart
  const prepareChartData = () => {
    // Group expenses by category and sum amounts
    const categoryTotals = {}
    
    expenses.forEach(expense => {
      if (!categoryTotals[expense.category]) {
        categoryTotals[expense.category] = 0
      }
      categoryTotals[expense.category] += expense.amount
    })
    
    // Convert to Chart.js format
    return {
      labels: Object.keys(categoryTotals),
      datasets: [{
        data: Object.values(categoryTotals),
        backgroundColor: [
          '#3B82F6', '#10B981', '#F59E0B', 
          '#8B5CF6', '#EF4444', '#06B6D4', '#F97316'
        ]
      }]
    }
  }

  // Calculate current month spending
  const getCurrentMonthSpending = () => {
    const now = new Date()
    const currentMonth = now.getMonth()
    const currentYear = now.getFullYear()
    
    return expenses
      .filter(expense => {
        const expenseDate = new Date(expense.date)
        return expenseDate.getMonth() === currentMonth && expenseDate.getFullYear() === currentYear
      })
      .reduce((total, expense) => total + expense.amount, 0)
  }

  // Prepare gauge chart data
  const prepareGaugeData = () => {
    const spent = getCurrentMonthSpending()
    const remaining = Math.max(0, monthlyBudget - spent)
    const percentage = (spent / monthlyBudget) * 100
    
    return {
      spent: spent.toFixed(2),
      remaining: remaining.toFixed(2),
      percentage: percentage.toFixed(0),
      color: percentage < 70 ? '#10B981' : percentage < 90 ? '#F59E0B' : '#EF4444'
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
            {/* Loop through categories array and create option for each */}
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
        <div className="insights-grid">
          <div className="stat-card">
            <p className="stat-label">Average Spending</p>
            <p className="stat-value">${insights.average_spending.toFixed(2)}</p>
          </div>
          <div className="stat-card">
            <p className="stat-label">Highest Expense</p>
            <p className="stat-value">${insights.highest_expense.toFixed(2)}</p>
          </div>
          <div className="stat-card">
            <p className="stat-label">Top Category</p>
            <p className="stat-value">{insights.most_common_category}</p>
            <p className="stat-subtext">{insights.category_count} expenses</p>
          </div>
        </div>
      )}

      {/* Budget Tracker */}
      <div className="budget-container">
        <h2>Monthly Budget</h2>
        <div className="budget-update">
          <input
            type="number"
            step="0.01"
            placeholder="Enter new budget"
            value={budgetInput}
            onChange={(e) => setBudgetInput(e.target.value)}
          />
          <button onClick={handleBudgetUpdate}>Update Budget</button>
        </div>
        <div className="budget-info">
          <p className="budget-amount">Budget: ${monthlyBudget.toFixed(2)}</p>
          <p className="spent-amount">Spent: ${prepareGaugeData().spent}</p>
          <p className="remaining-amount">Remaining: ${prepareGaugeData().remaining}</p>
        </div>
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{
              width: `${Math.min(prepareGaugeData().percentage, 100)}%`,
              backgroundColor: prepareGaugeData().color
            }}
          >
            <span className="progress-text">{prepareGaugeData().percentage}%</span>
          </div>
        </div>
      </div>

      {/* Chart Section - show spending by category */}
      <div className="chart-container">
        <h2>Spending by Category</h2>
        {expenses.length > 0 ? (
          <Pie data={prepareChartData()} />
        ) : (
          <p>Add expenses to see chart</p>
        )}
      </div>

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
                    {/* onclick passes expense.id to handleDelete */}
                    <button onClick={() => handleDelete(expense.id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Footer */}
      <footer className="footer">
        <p>Personal Project • Celeste Lomeli</p>
      </footer>
    </div>
  )
}

export default App
