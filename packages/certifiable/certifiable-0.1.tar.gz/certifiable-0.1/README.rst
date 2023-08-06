===========
Certifiable
===========

TODO: DISABLE WITH ENVVAR.


.. image:: https://img.shields.io/badge/Author:%20francis%20horsman-Available-brightgreen.svg?style=plastic
    :target: https://www.linkedin.com/in/francishorsman

.. image:: https://img.shields.io/pypi/v/certifiable.svg
    :target: https://pypi.python.org/pypi/certifiable
        :alt: PyPi version

.. image:: https://img.shields.io/travis/sys-git/certifiable.svg
    :target: https://travis-ci.org/sys-git/certifiable
        :alt: CI Status

.. image:: https://coveralls.io/repos/github/sys-git/certifiable/badge.svg
    :target: https://coveralls.io/github/sys-git/certifiable
        :alt: Coverage Status

.. image:: https://badge.fury.io/py/certifiable.svg
    :target: https://badge.fury.io/py/certifiable

.. image:: https://img.shields.io/pypi/l/certifiable.svg
    :target: https://img.shields.io/pypi/l/certifiable.svg

.. image:: https://img.shields.io/pypi/wheel/certifiable.svg
    :target: https://img.shields.io/pypi/wheel/certifiable.svg

.. image:: https://img.shields.io/pypi/pyversions/certifiable.svg
    :target: https://img.shields.io/pypi/pyversions/certifiable.svg

.. image:: https://img.shields.io/pypi/status/certifiable.svg
    :target: https://img.shields.io/pypi/status/certifiable.svg

.. image:: https://readthedocs.org/projects/certifiable/badge/?version=latest
    :target: https://certifiable.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/sys-git/certifiable/shield.svg
    :target: https://pyup.io/repos/github/sys-git/certifiable/
    :alt: Updates

Certifiable is a powerful runtime parameter validation library for python.

Features
--------
--------

Examples of all features can be found here: :ref:`usage`.

Core types
----------

It can validate the following *core* types

* Text
* Unicode
* String
* Bytes
* Bool
* Int
* Long
* Number
* Decimal
* Float
* Enum
* Enum value
* Timestamp
* Date
* Time
* Object


Complex types
-------------

There are more `complex` or compound types into which you can pass `other` certifiers:

* List
* Tuple
* Set
* Iterable
* Dict
* Json
* Html
* Email


Operators
---------

There are logical operators to combine certifiers:


* ANY   (certify_only_one)
* AND   (certify_all)
* ALL   (certify_all)
* NAND  (certify_none)
* XOR   (certify_only_one)

Custom Certifier
----------------

Use the `make_certifier` decorator and (optionally) bake-in some args and kwargs (any return value
from a certifier is ignored) to create your own certifier (first arg must be the value to certify):

>>> @make_certifier
... def my_certifier(value, *baked_args, **baked_kwargs):
...     print value
...     print baked_args
...     print baked_kwargs
...     baked_kwargs['data'].append('green')
...     if len(baked_kwargs['data'])==2:
...         raise MyError('damn!')

>>> args_to_bake = ('eggs', 'ham')
>>> kwargs_to_bake = dict(spam='lots', data=[])
>>> certifier = my_certifier(*args_to_bake, **kwargs_to_bake)

certifier can now be used as an argument to other certifiers.

>>> certify_list(
...     [1,'a'],
...     certifier=certifiers,
...     min_len=2,
...     max_len=5,
...     required=True,
... )
1
('eggs', 'ham')
{'spam': 'lots', data: []}
'a'
('eggs', 'ham')
{'spam': 'lots', data: ['green']}
Traceback (most recent call last):
    ...
    ...
    ...
MyError: damn!


Status
------

* Free software: MIT license
* Documentation: https://certifiable.readthedocs.io.
