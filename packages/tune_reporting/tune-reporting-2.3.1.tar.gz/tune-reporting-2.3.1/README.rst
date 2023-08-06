.. -*- mode: rst -*-

tune-reporting-python
---------------------

Python helper library for TUNE services.

The utility focus of this Python SDK is upon the TMC Reporting endpoints.


Badges
------

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |license|
    * - tests
      - |travis| |coveralls|
    * - package
      - |version| |supported-versions|

.. |docs| image:: https://readthedocs.org/projects/tune-reporting-python/badge/?style=flat
    :alt: Documentation Status
    :target: https://readthedocs.org/projects/tune-reporting-python

.. |license| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :alt: License Status
    :target: https://opensource.org/licenses/MIT

.. |travis| image:: https://travis-ci.org/TuneLab/tune-reporting-python.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/TuneLab/tune-reporting-python

.. |coveralls| image:: https://coveralls.io/repos/TuneLab/tune-reporting-python/badge.svg?branch=master&service=github
    :alt: Code Coverage Status
    :target: https://coveralls.io/r/TuneLab/tune-reporting-python

.. |requires| image:: https://requires.io/github/TuneLab/tune-reporting-python/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/TuneLab/tune-reporting-python/requirements/?branch=master

.. |version| image:: https://img.shields.io/pypi/v/tune_reporting.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/tune_reporting

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/tune_reporting.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/tune_reporting

.. end-badges


Install
-------

.. code-block:: bash

    pip install tune_reporting

Requirements
------------

:Prerequisites: Python 3.0
:API Key: To use SDK, it requires you to `Generate API Key <https://developers.tune.com/management-docs/resource-authentication-user-permissions//>`_


Run Examples
------------

.. code-block:: bash

    make run-examples tmc_api_key=[TMC API KEY]


Run Tests
---------

.. code-block:: bash

    make test tmc_api_key=[TMC API KEY]


License
-------

`MIT License <http://opensource.org/licenses/MIT>`_.