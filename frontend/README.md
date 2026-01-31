# Frontend - Expense Tracker

React + Vite frontend for the Expense Tracker application.

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Axios** - HTTP client for API requests
- **CSS** - Custom styling (no framework)

## Project Structure

```
src/
├── App.jsx          # Main component with all UI logic
├── App.css          # Component styles
├── index.css        # Global styles
└── main.jsx         # Entry point
```

## Development

**Install dependencies:**
```bash
npm install
```

**Start dev server:**
```bash
npm run dev
```

Runs on http://localhost:5173

**Backend must be running:**
```bash
# From project root
docker-compose up -d db backend
```

## Build for Production

```bash
npm run build
```

Outputs to `dist/` folder.

## Key Features

- Add expenses with date, category, amount, description
- View all expenses in a table
- See spending insights (average, highest, most common category)
- Delete expenses
- Real-time updates after actions
- Responsive design

## API Integration

Connects to FastAPI backend at `http://localhost:8000/api`

**Endpoints used:**
- `GET /api/expenses` - Fetch all expenses
- `POST /api/expenses` - Create expense
- `DELETE /api/expenses/{id}` - Delete expense
- `GET /api/insights` - Get analytics
- `GET /api/categories` - Get valid categories

## State Management

Uses React hooks:
- `useState` - Component state; store data that can change
- `useEffect` - Fetch data on mount; run code at specific times 

No external state management library needed for app size.
