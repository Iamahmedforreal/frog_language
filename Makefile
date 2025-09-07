
# Forg Language Compiler Makefile
# Provides convenient commands for development and testing

.PHONY: help install test clean run debug lint format docs

# Default target
help:
	@echo "Forg Language Compiler - Available Commands:"
	@echo ""
	@echo "  install     Install dependencies"
	@echo "  test        Run all tests"
	@echo "  test-unit   Run unit tests only"
	@echo "  test-files  Run file-based integration tests"
	@echo "  clean       Clean generated files"
	@echo "  run         Run compiler with default test file"
	@echo "  debug       Run compiler with all debug output"
	@echo "  lint        Run code linting (requires flake8)"
	@echo "  format      Format code (requires black)"
	@echo "  docs        Generate documentation (requires sphinx)"
	@echo "  benchmark   Run performance benchmarks"
	@echo ""
	@echo "Examples:"
	@echo "  make run FILE=tests/test1.forg"
	@echo "  make debug FILE=tests/test2.forg"

# Install dependencies
install:
	pip install -r requirements.txt

# Run all tests
test:
	python test_runner.py

# Run unit tests only
test-unit:
	python -m unittest discover -s . -p "*test*.py" -v

# Run file-based integration tests
test-files:
	@echo "Running integration tests on test files..."
	python main.py tests/test1.forg
	python main.py tests/test2.forg
	python main.py tests/test3.forg
	python main.py tests/test4.forg

# Clean generated files
clean:
	rm -rf __pycache__/
	rm -rf debug/*.json debug/*.ll
	rm -rf output/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

# Run compiler with default test file
run:
	python main.py $(if $(FILE),$(FILE),tests/test3.forg)

# Run compiler with debug output
debug:
	python main.py --debug-all $(if $(FILE),$(FILE),tests/test3.forg)

# Run compiler without execution
compile-only:
	python main.py --no-run $(if $(FILE),$(FILE),tests/test3.forg)

# Run linting (requires flake8)
lint:
	@which flake8 > /dev/null || (echo "flake8 not found. Install with: pip install flake8" && exit 1)
	flake8 --max-line-length=100 --ignore=E203,W503 *.py

# Format code (requires black)
format:
	@which black > /dev/null || (echo "black not found. Install with: pip install black" && exit 1)
	black --line-length=100 *.py

# Generate documentation (requires sphinx)
docs:
	@which sphinx-build > /dev/null || (echo "sphinx not found. Install with: pip install sphinx sphinx-rtd-theme" && exit 1)
	mkdir -p docs
	sphinx-quickstart -q -p "Forg Compiler" -a "Forg Team" -v "1.0" --ext-autodoc --ext-viewcode docs
	sphinx-build -b html docs docs/_build

# Run performance benchmarks
benchmark:
	python main.py --benchmark tests/test3.forg
	python main.py --benchmark tests/test4.forg

# Development setup
dev-setup: install
	@echo "Setting up development environment..."
	@echo "Installing optional development dependencies..."
	pip install pytest pytest-cov black flake8 mypy
	@echo "Development environment ready!"

# Create a new test file template
new-test:
	@read -p "Enter test name: " name; \
	echo "fn main() -> int {" > tests/test_$$name.forg; \
	echo "    // TODO: Add test code here" >> tests/test_$$name.forg; \
	echo "    return 0;" >> tests/test_$$name.forg; \
	echo "}" >> tests/test_$$name.forg; \
	echo "Created tests/test_$$name.forg"

# Show project statistics
stats:
	@echo "Forg Compiler Project Statistics:"
	@echo "================================="
	@echo "Python files: $$(find . -name '*.py' | wc -l)"
	@echo "Forg test files: $$(find tests -name '*.forg' | wc -l)"
	@echo "Lines of Python code: $$(find . -name '*.py' -exec cat {} \; | wc -l)"
	@echo "Lines of Forg code: $$(find tests -name '*.forg' -exec cat {} \; | wc -l)"
	@echo ""
	@echo "Recent commits:"
	@git log --oneline -5 2>/dev/null || echo "Not a git repository"
