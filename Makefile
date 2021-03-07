SHELL := /bin/bash

.PHONY: docs clean

VENV_NAME = .venv
VENV_BIN_PATH = $(VENV_NAME)/bin
PYTHON_PATH = $(VENV_NAME)/bin/python
PIP_PATH = $(VENV_NAME)/bin/pip

REQUIREMENTS_FILE = requirements.txt

MANAGE_COMMAND = $(VENV_BIN_PATH)/python manage.py --load-env

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

venv:
	python3 -m venv $(VENV_NAME)

migration:
	$(MANAGE_COMMAND) makemigrations

migrate:
	$(MANAGE_COMMAND) migrate

loaddata:
	$(MANAGE_COMMAND) loaddata data.yaml

dumpdata:
	$(MANAGE_COMMAND) dumpdata --format yaml > data.yaml

superuser:
	$(MANAGE_COMMAND) createsuperuser

collectstatic:
	$(MANAGE_COMMAND) collectstatic --no-input

clean:
	rm -rf build
	rm -rf hello.egg-info
	rm -rf dist
	rm -rf htmlcov
	rm -rf .tox
	rm -rf .cache
	rm -rf .pytest_cache
	find . -type f -name "*.pyc" -delete
	rm -rf $(find . -type d -name __pycache__)
	rm .coverage
	rm .coverage.*

install:
	$(PIP_PATH) install -r $(REQUIREMENTS_FILE)
