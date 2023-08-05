Buffered SMTP Logging Handler
=============================

|PYPIVersion| |PythonVersions| |BuildStatus| |Coveralls|

A library that mimics the standard ``logging.handlers.SMTPHandler`` class but sends email messages only when a preconfigured buffer is full or on exit.

Installation and dependencies
-----------------------------

Install the program using pip:

.. code::

  pip install buffered_smtp_handler

How to use it
-------------

This library offers two classes: ``BufferedSMTPHandler`` and ``BufferedSMTPHandlerSSL``.

They accept the same arguments of the `standard SMTPHandler class <https://docs.python.org/2/library/logging.handlers.html#smtphandler>`__, and also the ``capacity`` argument to set the capacity of the buffer (default: 100).

The SSL version is based on the ``smtplib.SMTP_SSL`` and avoids to perform StartSSL.

Via code:

>>> import logging
>>> from pierky.buffered_smtp_handler import BufferedSMTPHandler
>>> logger = logging.getLogger("my_app")
>>> logger.setLevel(logging.INFO)
>>> h = BufferedSMTPHandler("smtp.example.com", "from@example.com", ["to@example.com"], "MyApp log", capacity=10)
>>> logger.addHandler(h)
>>> logger.warning("Test")

Via a `logging configuration file <https://docs.python.org/2/library/logging.config.html#logging-config-fileformat>`__:

.. code::

  [loggers]
  keys=root
  
  [formatters]
  keys=simple
  
  [handlers]
  keys=stderr,smtp
  
  [logger_root]
  level=INFO
  
  handlers=stderr,smtp
  
  [formatter_simple]
  format=ARouteServer %(asctime)s %(levelname)s %(message)s
  
  [handler_stderr]
  class=StreamHandler
  formatter=simple
  args=(sys.stderr,)
  
  [handler_smtp]
  class=pierky.buffered_smtp_handler.BufferedSMTPHandler
  level=WARN
  formatter=simple
  args=(('smtp.example.com', 25), 'from@example.com', ['to@example.com'], 'MyApp log')


Author
------

Pier Carlo Chiodi - https://pierky.com/

Blog: https://blog.pierky.com/ Twitter: `@pierky <https://twitter.com/pierky>`_

.. |PYPIVersion| image:: https://img.shields.io/pypi/v/buffered_smtp_handler.svg
    :target: https://pypi.python.org/pypi/buffered_smtp_handler/
.. |PythonVersions| image:: https://img.shields.io/pypi/pyversions/buffered_smtp_handler.svg
.. |BuildStatus| image:: https://travis-ci.org/pierky/bufferedsmtphandler.svg?branch=master
    :target: https://travis-ci.org/pierky/bufferedsmtphandler
.. |Coveralls| image:: https://coveralls.io/repos/github/pierky/bufferedsmtphandler/badge.svg?branch=master
    :target: https://coveralls.io/github/pierky/bufferedsmtphandler?branch=master
