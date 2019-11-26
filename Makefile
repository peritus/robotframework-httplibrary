VERSION = 1.1.0

.PHONY: tests
tests:
	tox

.PHONY: clean
clean:
	git clean -dfx

.PHONY: run-robotframework
run-robotframework:
	bin/robotframework tests

.PHONY: buildout-development-py2
buildout-development-py2:
	virtualenv --no-site-packages .venv27
	.venv27/bin/python bootstrap.py
	bin/buildout

.PHONY: buildout-development-py3
buildout-development-py3:
	virtualenv --no-site-packages --python=python3 .venv36
	.venv36/bin/python bootstrap.py
	bin/buildout
