#!/usr/bin/make
.PHONY: install clean test run

install:
	pipenv --three install -e ".[testing]"

run:
	pipenv run pserve --reload development.ini

test:
	pipenv run pytest -qs

clean:
	pipenv clean && rm -rf memory.egg-info/
