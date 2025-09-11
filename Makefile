.PHONY: help install install-dev run test lint format clean docker-build docker-run docker-stop

help:
	@echo "Available commands:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  run          Run the Streamlit application"
	@echo "  test         Run tests"
	@echo "  lint         Run linting checks"
	@echo "  format       Format code with black and isort"
	@echo "  clean        Clean up temporary files"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run   Run with Docker Compose"
	@echo "  docker-stop  Stop Docker containers"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

run:
	streamlit run app.py

test:
	pytest tests/ -v --cov=.

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	black .
	isort .

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .coverage

docker-build:
	docker compose -f config/docker-compose.yml build

docker-run:
	docker compose -f config/docker-compose.yml up -d

docker-stop:
	docker compose -f config/docker-compose.yml down

docker-logs:
	docker compose -f config/docker-compose.yml logs -f

# Data management
fetch-data:
	python scripts/fetch_top10_stocks.py

update-tickers:
	python scripts/update_top10_tickers.py

# Development
dev-setup: install-dev
	pre-commit install

dev-run:
	streamlit run app.py --server.runOnSave true
