STATEDIR = $(PWD)/.state

.PHONY: clean clean-test clean-pyc clean-build help
.DEFAULT_GOAL := help

# Create a marker file for the docker-build
$(STATEDIR)/docker-build: Dockerfile requirements.txt
	# Build our docker container(s) for this project.
	docker-compose build

	# Mark the state so we don't rebuild this needlessly.
	mkdir -p $(STATEDIR)
	touch $(STATEDIR)/docker-build

cnx_slim_dump.sql.gz:
	scp backup2.cnx.org:`ssh backup2.cnx.org 'ls -t /var/backups/cnx_slim_dump.*.sql.gz | awk "{print $1; exit}"'` cnx_slim_dump.sql.gz


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

test-webview: cnx_slim_dump.sql.gz $(STATEDIR)/docker-build
	docker-compose up -d selenium-chrome
	docker-compose exec selenium-chrome wait-for db:5432 -t 900 -- tox -- --new-first --failed-first --webview_base_url=http://ui:8000 --archive_base_url=http://archive:6543 -m "webview and not (requires_complete_dataset or requires_deployment or requires_varnish_routing or legacy)"

venv:
	python3 -m venv .venv && \
		source .venv/bin/activate && \
		pip install -r requirements.txt

ci-test-webview:
	docker-compose -f docker-compose.test.yml up -d
	docker-compose -f docker-compose.test.yml exec -T -e ARCHIVE_BASE_URL=https://archive-staging.cnx.org -e LEGACY_BASE_URL=https://legacy-staging.cnx.org -e WEBVIEW_BASE_URL=https://staging.cnx.org selenium-chrome tox -- --new-first --failed-first -m "webview"

ci-test: ci-test-webview ## run all ci-test-* recipes

help:
	@echo "The following targets are available"
	@echo "clean			Remove build, test, and file artifacts"
	@echo "clean-build 		Remove build artifacts"
	@echo "clean-pyc		Remove file artifacts"
	@echo "clean-state		Remove make's build state"
	@echo "clean-test		Remove test artifacts"
	@echo "test-webview		Runs the webview tests in an contained environment"
	@echo "--------------------------------------------------------------------------------"
	@echo "ci-test			Runs all ci-test-* make recipes"
	@echo "ci-test-webview		Runs the webview tests in a CI environment"
