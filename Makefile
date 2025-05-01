.PHONY: clean test coverage help code-run code-help

# Default
default: coverage

clean:
	# remove coverage reports
	rm -rf htmlcov .coverage
	# remove pytest cache
	rm -rf .pytest_cache
	# remove all Python byte-code caches
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Install runtime dependencies
install:
	pip install -r requirements.txt

# Install development dependencies (tests, linters, etc.)
install-dev: install
	pip install -r requirements-dev.txt

# Run tests quickly
test:
	pytest

# Run tests with coverage reports
coverage:
	pytest --cov=src --cov-report=term --cov-report=html tests/

# Help
help:
	@echo "Available commands:"
	@echo "  make          Run coverage tests (default)"
	@echo "  make clean    Remove caches and reports"
	@echo "  make install       Install runtime deps"
	@echo "  make install-dev   Install runtime + dev deps"
	@echo "  make test     Run quick tests only"
	@echo "  make coverage Run tests with coverage report"
	@echo "  make code-run Run the application"
	@echo "  make code-help Show --help output for the application"

# Show the --help output
code-help:
	PYTHONPATH=src python src/cms/main.py --help

# Run the main application
run:
	./bin/cube $(ARGS)
