.PHONY: upload test register release

release: test register upload

register:
	python setup.py register

upload:
	python setup.py sdist upload

test:
	tox
