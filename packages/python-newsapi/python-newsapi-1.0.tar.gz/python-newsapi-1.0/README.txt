NewsAPI python wrapper
======================

Python wrapper for `newsapi.org <https://newsapi.org/>`__ api.

Install
-------

::

    pip install https://github.com/cyriac/python-newsapi/archive/master.zip

Usage
-----

.. code:: python

    from newsapi import NewsAPI

    key = 'your key goes here'
    params = {}

    api = NewsAPI(key)
    sources = api.sources(params)
    articles = api.articles(sources[0]['id'], params)

