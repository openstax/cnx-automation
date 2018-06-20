.PHONY: clean clean-test clean-pyc clean-build help
.DEFAULT_GOAL := help

clean: clean-build clean-pyc clean-test

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -fr assets/
	rm -f report.html

venv:
	python3 -m venv .venv && \
		source .venv/bin/activate && \
		pip install -r requirements.txt

help:
	@echo "The following targets are available"
	@echo "clean			Remove build, test, and file artifacts"
	@echo "clean-build 		Remove build artifacts"
	@echo "clean-pyc		Remove file artifacts"
	@echo "clean-test		Remove test artifacts"
