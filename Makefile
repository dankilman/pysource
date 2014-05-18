.PHONY: upload test register

release: test register upload

register:
	python setup.py register

upload:
	python setup.py sdist
	python setup.py upload

test:
	tox
