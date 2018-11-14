STATEDIR = $(PWD)/.state

.PHONY: clean clean-test clean-pyc clean-build venv help
.DEFAULT_GOAL := help


clean: clean-build clean-pyc clean-state clean-test

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

clean-state: ## remove the build state
	rm -rf $(STATEDIR)

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -fr assets/
	rm -f report.html

venv:
	python3 -m venv .venv && \
		source .venv/bin/activate && \
		pip install -r requirements.txt

precommit:
	pre-commit install


help:
	@echo "The following targets are available"
	@echo "clean			Remove build, test, and file artifacts"
	@echo "clean-build 		Remove build artifacts"
	@echo "clean-pyc		Remove file artifacts"
	@echo "clean-state		Remove make's build state"
	@echo "clean-test		Remove test artifacts"
	@echo "venv			Set up a virtualenv for this project"
