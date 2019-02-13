Documentation
=============

Imio memory app. In this application, you can save some json data into persistant DB.


Installation
------------
If pipenv is not installed, install it (`sudo pip install pipenv`).

And after, you can use this command:

    make install

Dev
---
Run application with this command:

    make run

Tests
-----
Test app with:

    make test

.. image:: https://travis-ci.org/IMIO/imio.memory.png
    :target: http://travis-ci.org/IMIO/imio.memory

.. image:: https://coveralls.io/repos/github/IMIO/imio.memory/badge.svg?branch=master
    :target: https://coveralls.io/github/IMIO/imio.memory?branch=master

Add an app
----------

Add an application with curl command

    $ curl -X POST http://0.0.0.0:6543 -d '{"app_id": "newapp"}'
