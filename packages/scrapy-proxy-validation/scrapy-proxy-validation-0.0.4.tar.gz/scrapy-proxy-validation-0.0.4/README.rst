=======================
Scrapy-Proxy-Validation
=======================

.. image:: https://img.shields.io/pypi/v/scrapy-proxy-validation.svg
   :target: https://pypi.python.org/pypi/scrapy-proxy-validation
   :alt: PyPI Version

.. image:: https://img.shields.io/travis/grammy-jiang/scrapy-proxy-validation/master.svg
   :target: http://travis-ci.org/grammy-jiang/scrapy-proxy-validation
   :alt: Build Status

.. image:: https://img.shields.io/badge/wheel-yes-brightgreen.svg
   :target: https://pypi.python.org/pypi/scrapy-proxy-validation
   :alt: Wheel Status

.. image:: https://img.shields.io/codecov/c/github/grammy-jiang/scrapy-proxy-validation/master.svg
   :target: http://codecov.io/github/grammy-jiang/scrapy-proxy-validation?branch=master
   :alt: Coverage report

Overview
========

Scrapy is a great framework for web crawling. This package provides a highly
customized way to deal with the exceptions happening in the downloader
middleware because of the proxy, and uses a signal to note relatives to treat
the invalidated proxies (e.g. moving to blacklist, renew the proxy pool).

There are two types of signals this package support:

* traditional signal, sync

* deferred signal, async

Please refer to the scrapy and twisted documents:

* `Core API — Scrapy 1.4.0 documentation`_

.. _`Core API — Scrapy 1.4.0 documentation`: https://doc.scrapy.org/en/latest/topics/api.html#topics-api-signals

* `Signals — Scrapy 1.4.0 documentation`_

.. _`Signals — Scrapy 1.4.0 documentation`: https://doc.scrapy.org/en/latest/topics/signals.html

* `Deferred Reference — Twisted 17.9.0 documentation`_

.. _`Deferred Reference — Twisted 17.9.0 documentation`: https://twistedmatrix.com/documents/current/core/howto/defer.html

Requirements
============

* Scrapy

* Tests on Python 3.5

* Tests on Linux, but it is a pure python module, should work on any other
  platforms with official python and twisted support

Installation
============

The quick way::

   pip install -U scrapy-proxy-validation

Or put this middleware just beside the scrapy project.

Documentation
=============

Set this middleware in ``ITEMPIPELINES`` in ``settings.py``, for example::

    from scrapy_proxy_validation.downloadermiddlewares.proxy_validation import Validation

    DOWNLOADER_MIDDLEWARES.update({
        'scrapy_proxy_validation.downloadmiddlewares.proxy_validation.ProxyValidation': 751
    })

    SIGNALS = [Validation(exception='twisted.internet.error.ConnectionRefusedError',
                          signal='scrapy.signals.spider_closed'),
               Validation(exception='twisted.internet.error.ConnectionLost',
                          signal='scrapy.signals.spider_closed',
                          signal_deferred='scrapy.signals.spider_closed',
                          limit=5)]

    RECYCLE_REQUEST = 'scrapy_proxy_validation.utils.recycle_request.recycle_request'


Settings Reference
==================

SIGNALS
-------

A list of the class Validation with the exception it wants to deal with, the
sync signal it sends, the async signal it sends and the limit it touches.

RECYCLE_REQUEST
---------------

A function to recycle the request which have trouble with the proxy, the input
argument is ``request``, and the output is ``request`` too.

**Note: remember to set ``dont_filter`` to be ``True``, or the middleware
``duplicate_fitler`` will remove this request.**

Built-in Functions
==================

scrapy_proxy_validation.utils.recycle_request.recycle_request
-------------------------------------------------------------

This is a built-in function to recycle the request which has a problem with
the proxy.

This function will remove the proxy keyword in meta and set ``dont_filter`` to
be ``True``.

To use this function, in ``settings.py``::

    RECYCLE_REQUEST = 'scrapy_proxy_validation.utils.recycle_request.recycle_request'

Note
====

There could be many different problems about the proxy, thus it will take some
to collect them all and add to ``SIGNALS``. Please be patient, this is not a
once-time solution middleware for this case.

TODO
====

No idea, please let me know if you have!
