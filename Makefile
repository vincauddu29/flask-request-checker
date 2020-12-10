uninstall:
	- pip3 uninstall requestChecker -y
	- rm -rf dist/
	- rm -rf build/

build:
	python3 setup.py sdist bdist_wheel

install: build uninstall
	pip3 install .

test: clean_coverage
	@echo 'Running all tests...'
	coverage run --source=src/requestChecker --module pytest
	coverage report

clean_coverage:
	@rm -f .coverage

clean:
	@rm -f src/requestChecker/*.pyc

pep8:
	@echo 'Checking pep8 compliance...'
	@pycodestyle src/requestChecker/* tests/*.py

pyflakes:
	@echo 'Running pyflakes...'
	@pyflakes src/requestChecker/* tests/*.py

check: clean pep8 pyflakes test