Welcome to ``pynano``
=====================

.. image:: https://readthedocs.org/projects/pynano/badge/?version=latest
   :target: http://pynano.readthedocs.org/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://readthedocs.org/projects/pynano/badge/?version=stable
   :target: http://pynano.readthedocs.org/en/stable/?badge=stable
   :alt: Documentation Status

.. image:: https://img.shields.io/travis/Kromey/pynano.svg
   :target: https://travis-ci.org/Kromey/pynano
   :alt: Build Status

.. image:: https://img.shields.io/codecov/c/github/Kromey/pynano.svg
   :target: https://codecov.io/github/Kromey/pynano?branch=master
   :alt: Code Coverage

`National Novel Writing Month <https://nanowrimo.org>`_ is an annual event in
which the goal is generally to write 50,000 words of the first draft of a novel
in the 30 days of November.

Naturally, the hosts have graciously supplied a website with various means of
updating and tracking one's progress through this adventure, including an `API
<https://nanowrimo.org/wordcount_api>`_ to allow users to create their own
progress trackers.

This is where ``pynano`` comes into play, providing a simple, Pythonic way to
acess this API and leverage its data in your own projects::

   >>> from pynano import User
   >>> kromey = User('kromey')
   >>> kromey.wordcount
   64133
   >>> kromey.name
   'Kromey'

Objects are provided to access data about Users, Regions, and the Site itself;
each also provides access to daily data to track progress through the month::

   >>> kromey.history[14].date # The sequence is 0-indexed, so index 14 is day 15
   '2015-11-15'
   >>> kromey.history[14].wordcount
   10499

Requirements
------------

``pynano`` is supported on Python versions 2.7, 3.5, and 3.6, with these
additional packages:

* requests (version 2.9 or later)
* xmltodict (version 0.9 or later)

.. note::

   ``pynano`` is also tested against Python versions 3.3, and 3.4, though
   they are not officially supported. As a convenience, however, they remain
   listed on PyPi as long as they continue to pass tests.

