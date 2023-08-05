ws_sheets
=========
.. image:: https://travis-ci.org/chuck1/ws_sheets.svg?branch=master
    :target: https://travis-ci.org/chuck1/ws_sheets
.. image:: https://codecov.io/gh/chuck1/ws_sheets/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/chuck1/ws_sheets
.. image:: https://readthedocs.org/projects/ws_sheets/badge/?version=latest
   :target: http://ws_sheets.readthedocs.io/
   :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/ws_sheets.svg
   :target: https://pypi.python.org/pypi/ws_sheets
.. image:: https://img.shields.io/pypi/pyversions/ws_sheets.svg
   :target: https://pypi.python.org/pypi/ws_sheets

Python module defining spreadsheet-like objects in which
cell and script inputs are pure python code.

Install
-------

::

    pip3 install ws_sheets

Test
----

::

    git clone git@github.com:chuck1/ws_sheets
    cd ws_sheets
    pip3 install -e .
    pytest

Example
-------

.. testcode::
    
    import modconf
    settings = modconf.import_conf('ws_sheets.tests.conf.simple').Settings

    from ws_sheets import Book

    book = Book(settings)
    
    book['0'][0, 0] = '1'
    book['0'][0, 1] = '2'
    book['0'][0, 2] = '3'
    book['0'][0, 3] = "book['0'][0, 0:3]"
    book['0'][0, 4] = "sum(book['0'][0, 3])"
    
    print(book['0'][0, 3])
    print(book['0'][0, 4])

Output:

.. testoutput::
    
    [1 2 3]
    6

