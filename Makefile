#!/usr/bin/make
.PHONY: install clean test run

install:
	pipenv --three install -e ".[testing]"

run:
	pipenv run pserve --reload development.ini

test:
	pipenv run pytest -qs

coverage:
	pipenv run pytest --cov=memory

clean:
	pipenv clean && rm -rf memory.egg-info/ && rm -rf .pytest_cache

docker-image:
	docker build --no-cache -t imio/memory:latest .
