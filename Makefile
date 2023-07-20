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

.PHONY: run service with default profile
run:
	poetry run uvicorn hf_serve.main:app 

.PHONY: use curl to test the feature extraction service
run-feature-extraction:
	HF_SERVE_TASK=feature-extraction poetry run uvicorn hf_serve.main:app 

.PHONY: use curl to test the text classification service
text-classification:
	curl -X POST http://localhost:8000 -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"data": "Je deteste la reforme des retraites"}'



batch-text-classification:
	seq 100 | xargs -I{} curl -X POST http://localhost:8000 -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"data": "Je deteste la reforme des retraites"}'

fmt:
	poetry run black hf_serve tests
	poetry run isort hf_serve tests

