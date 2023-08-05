openapi-core
************

.. image:: https://img.shields.io/pypi/v/openapi-core.svg
     :target: https://pypi.python.org/pypi/openapi-core
.. image:: https://travis-ci.org/p1c2u/openapi-core.svg?branch=master
     :target: https://travis-ci.org/p1c2u/openapi-core
.. image:: https://img.shields.io/codecov/c/github/p1c2u/openapi-core/master.svg?style=flat
     :target: https://codecov.io/github/p1c2u/openapi-core?branch=master
.. image:: https://img.shields.io/pypi/pyversions/openapi-core.svg
     :target: https://pypi.python.org/pypi/openapi-core
.. image:: https://img.shields.io/pypi/format/openapi-core.svg
     :target: https://pypi.python.org/pypi/openapi-core
.. image:: https://img.shields.io/pypi/status/openapi-core.svg
     :target: https://pypi.python.org/pypi/openapi-core

About
=====

Openapi-core is a Python library that adds client-side and server-side support
for the `OpenAPI Specification v3.0.0 <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md>`__.

Installation
============

Recommended way (via pip):

::

    $ pip install openapi-core

Alternatively you can download the code and install from the repository:

.. code-block:: bash

   $ pip install -e git+https://github.com/p1c2u/openapi-core.git#egg=openapi_core


Usage
=====

Firstly create your specification:

.. code-block:: python

   from openapi_core import create_spec

   spec = create_spec(spec_dict)

Now you can use it to validate and unmarshal requests

.. code-block:: python

   from openapi_core import request_parameters_factory, request_body_factory

   parameters = request_parameters_factory.create(request, spec)
   body = request_body_factory.create(request, spec)

Related projects
================
* `openapi-spec-validator <https://github.com/p1c2u/openapi-spec-validator>`__


