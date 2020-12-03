uninstall:
	- pip3 uninstall requestChecker -y
	- rm -rf dist/
	- rm -rf build/

build:
	python3 setup.py sdist bdist_wheel

install: build uninstall
	pip3 install .