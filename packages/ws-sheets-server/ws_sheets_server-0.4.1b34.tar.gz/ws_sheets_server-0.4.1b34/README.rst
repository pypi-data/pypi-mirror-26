ws_sheets_server
================
.. image:: https://travis-ci.org/chuck1/ws_sheets_server.svg?branch=master
    :target: https://travis-ci.org/chuck1/ws_sheets_server
.. image:: https://codecov.io/gh/chuck1/ws_sheets_server/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/chuck1/ws_sheets_server
.. image:: https://readthedocs.org/projects/ws_sheets_server/badge/?version=latest
   :target: http://ws_sheets_server.readthedocs.io/
   :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/ws_sheets_server.svg
   :target: https://pypi.python.org/pypi/ws_sheets_server
.. image:: https://img.shields.io/pypi/pyversions/ws_sheets_server.svg
   :target: https://pypi.python.org/pypi/ws_sheets_server

Server program that reads ws_sheets.Book object from storage, executes those objects
and returns the results to a client.

Install
-------

::

    pip3 install ws_sheets_server

Test
----

::

    git clone git@github.com:chuck1/ws_sheets_server
    cd ws_sheets_server
    pip3 install -r requirements.txt
    pip3 install -e .
    pytest

Run
---

::

    ws_sheets_server runserver ws_sheets_server.tests.conf.simple --dev

