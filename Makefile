.PHONY: run test coverage clean docker-up docker-down docker-build

# Default target
all: help

# Help target to show available commands
help:
	@echo "Available commands:"
	@echo "  make run        - Run the backend server"
	@echo "  make test       - Run all tests"
	@echo "  make coverage   - Run tests with coverage report"
	@echo "  make clean      - Clean up generated files"
	@echo "  make docker-up  - Start Docker containers"
	@echo "  make docker-down - Stop Docker containers"
	@echo "  make docker-build - Build Docker containers"

# Run the backend server
run:
	@echo "Starting backend server..."
	uvicorn src.presentation.api:app --reload --host 0.0.0.0 --port 8000

# Run all tests
test:
	@echo "Running tests..."
	pytest tests/ -v

# Run tests with coverage
coverage:
	@echo "Running tests with coverage..."
	pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Clean up generated files
clean:
	@echo "Cleaning up..."
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	rm -rf */__pycache__/
	rm -rf */*/__pycache__/

# Docker commands
docker-up:
	@echo "Starting Docker containers..."
	docker-compose up

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

docker-build:
	@echo "Building Docker containers..."
	docker-compose build 