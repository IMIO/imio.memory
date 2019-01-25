#!/usr/bin/make
.PHONY: buildout cleanall test instance

install:
	pipenv install -e ".[testing]"

run:
	pipenv run pserve --reload development.ini

test:
	pipenv run pytest -qs
