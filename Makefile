# Define the name of your project
PROJECT_NAME = hf-serve

# Define the virtual environment name
VENV_NAME = $(PROJECT_NAME)-venv

# Define phony targets
.PHONY: help
help:
	@echo "Makefile for $(PROJECT_NAME)"
	@echo ""
	@echo "Available commands:"
	@echo "  help       Display this help message"
	@echo "  install    Install dependencies"
	@echo "  test       Run tests"
	@echo "  clean      Remove build and cache files"
	@echo ""

.PHONY: install
install:
	poetry install

.PHONY: test
test:
	poetry run pytest

.PHONY: clean
clean:
	poetry run rm -rf build dist *.egg-info
	find . -name __pycache__ -type d -exec poetry run rm -rf {} +
	find . -name '*.pyc' -exec poetry run rm -f {} +
	find . -name '*.pyo' -exec poetry run rm -f {} +

.PHONY: venv
venv:
	poetry env use $(shell poetry env info --path)

# Define default target
.DEFAULT_GOAL := help

.PHONY: run example model server with starlette and uvicorn
run-starlette:
	poetry run uvicorn hf_serve.serving_starlette:app --reload

.PHONY: run example model server with fastapi and uvicorn
run-fastapi:
	poetry run uvicorn hf_serve.serving_fastapi:app --reload

.PHONY: use curl to test the server
curl:
	curl -X POST http://192.168.88.179 -d "Je deteste la reforme des retraites"