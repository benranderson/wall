.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

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
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check style with flake8
	flake8 wall tests

test: ## run tests
	py.test

test-all: ## run tests on every Python version with tox
	tox

cover: ## check code coverage
	pytest --cov-report term --cov-report html --cov=wall/ tests/ -v
	$(BROWSER) htmlcov/index.html

test-ci: ## test and check code coverage for Travis CI
	coverage run --source wall -m pytest tests/
	coverage report -m
	coverage html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/wall.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ wall
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

publish: clean ## build a wheel and an sdist (tarball) and upload to PyPI
	flit publish

dist: clean ## build a wheel and an sdist (tarball)
	flit build

install: clean ## install the package to the active Python's site-packages
	flit install

dinstall: clean ## install the package in development mode
	flit install -s

nb: ## initialise jupyter notebook
	jupyter notebook