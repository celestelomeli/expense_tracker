# Expense Tracker - Makefile

# .PHONY to distinguish commands from files
.PHONY: help start stop restart logs clean test frontend backend db

# Prints menu of available commands
help:
	@echo "Expense Tracker - Available Commands:"
	@echo ""
	@echo "  make start      - Start all services (database + backend)"
	@echo "  make frontend   - Start React frontend dev server"
	@echo "  make stop       - Stop all Docker containers"
	@echo "  make restart    - Restart all services"
	@echo "  make logs       - View logs from all containers"
	@echo "  make clean      - Stop containers and remove volumes (deletes data!)"
	@echo "  make db         - Access MySQL database shell"
	@echo "  make test       - Run tests (when implemented)"
	@echo ""

# Start database and backend
start:
	@echo "Starting database and backend..."
	docker-compose up -d db backend                 #run docker compose in detached mode 
	@echo "Services started!"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

# Start React frontend
frontend:
	@echo "Starting React frontend..."
	cd frontend && npm run dev

# Stop all containers
stop:
	@echo "Stopping all containers..."
	docker-compose down
	@echo "✓ Containers stopped"

# Restart all services
restart: stop start

# View logs
logs:
	docker-compose logs -f                           # Show logs and follow 

# Clean everything (remove data)
clean:
	@echo "This will delete all data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \  # Read only one character
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \         # Check if answer starts with Y or y
		docker-compose down -v; \               # Stop containers and remove volumes
		echo "Cleaned up"; \
	else \
		echo "Cancelled"; \
	fi

# Access database shell
db:
	@echo "Connecting to MySQL..."
	docker exec -it expense_tracker_db mysql -u root -p$$(grep DB_PASSWORD .env | cut -d '=' -f2) expense_tracker

# Run tests 
test:
	@echo "Running tests..."
	@echo "Tests not implemented yet"

# Build Docker images
build:
	@echo "Building Docker images..."
	docker-compose build
	@echo "Build complete"

# Install frontend dependencies
# Installs npm packages for React
install:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Dependencies installed"
