.PHONY: clean-pyc develop

help:
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "develop - build and create app"
	@echo "coverage - check code coverage quickly with the default Python"

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm -rf tuiuiusaas.egg-info dist build app

develop: clean-pyc
	pip install -e .[testing,docs]
	npm install && npm run build
	tuiuiu start app

lint:
	flake8 tuiuiu
	isort --check-only --diff --recursive tuiuiu

test:
	python runtests.py

test-all:
	tox

coverage:
	coverage run --source tuiuiu setup.py
	coverage report -m
	coverage html
	open htmlcov/index.html
