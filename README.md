# Expense Tracker

A command-line application to track daily expenses with summaries and insights. Built with Python, MySQL, and Docker.

## Features

- Add expenses with date, category, amount, and description
- View expense summaries grouped by date
- Generate insights (average spending, highest expense, most common category)
- Delete expenses by ID
- Input validation for dates and amounts
- Dockerized for easy setup and deployment

## Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)

## Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd expense_tracker
   ```

2. **Environment variables are already configured in `.env`**
   - The `.env` file contains database credentials
   - For production, update the password in `.env`

3. **Build and start the database:**
   ```bash
   docker-compose up -d db
   sleep 5  # Wait for database to initialize
   ```

4. **Run the application:**
   ```bash
   docker-compose run --rm app
   ```

## Usage

Once the app starts, you'll see a menu:

```
==============================
    EXPENSE TRACKER
==============================
1. Add Expense
2. View Summaries
3. Generate Insights
4. Delete Expense
5. Exit
==============================
```

### Adding an Expense

1. Choose option `1`
2. Enter date in `YYYY-MM-DD` format (e.g., `2026-01-30`)
3. Enter category (e.g., `Food`, `Transport`, `Bills`)
4. Enter amount (positive number, e.g., `25.50`)
5. Enter description (e.g., `Lunch at cafe`)

### Viewing Summaries

Choose option `2` to see total spending grouped by date.

### Generating Insights

Choose option `3` to see:
- Average spending across all expenses
- Highest single expense
- Most frequently used category

### Deleting an Expense

Choose option `4`, view all expenses with their IDs, and enter the ID to delete.

## Project Structure

```
expense_tracker/
├── src/
│   └── app.py              # Main application code
├── docker/
│   ├── Dockerfile          # App container configuration
│   ├── Dockerfile.mysql    # MySQL container configuration
│   └── init.sql           # Database initialization script
├── .env                    # Environment variables (not committed)
├── .env.example           # Environment template
├── docker-compose.yml     # Docker orchestration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Docker Commands

**Start database:**
```bash
docker-compose up -d db
```

**Run app interactively:**
```bash
docker-compose run --rm app
```

**Stop all containers:**
```bash
docker-compose down
```

**Stop and delete all data:**
```bash
docker-compose down -v
```

**View database directly:**
```bash
docker exec -it expense_tracker_db mysql -u root -p<password> -e "SELECT * FROM expense_tracker.expenses;"
```

## Development

**Run locally without Docker:**

1. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Update `.env` with local MySQL credentials

4. Run the app:
   ```bash
   python src/app.py
   ```

## Technologies Used

- **Python 3.11** - Application logic
- **MySQL 8.0** - Database
- **Docker** - Containerization
- **python-dotenv** - Environment variable management
- **mysql-connector-python** - Database connectivity

## License

MIT
