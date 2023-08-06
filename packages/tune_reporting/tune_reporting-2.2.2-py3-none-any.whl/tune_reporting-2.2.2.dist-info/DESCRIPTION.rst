.. -*- mode: rst -*-

tune-reporting-python
---------------------

    :package: `tune-reporting-python <https://github.com/TuneLab/tune-reporting-python>`_
    :label: TUNE Reporting Python SDK 3.0
    :purpose: Incorporate TUNE services.
    :update   2017-11-21 17:00:00 UTC
    :version: 3.0.0

Overview
--------

Python helper library for TUNE services.

The utility focus of this Python SDK is upon the Advertiser Reporting endpoints.

The second goal of the SDKs is to assure that our customers’ developers are using best practices in gathering reports in the most optimal way.

Please see documentation here: `TUNE Reporting API <https://developers.tune.com/reporting/>`_

.. start-badges

.. list-table::
    :stub-columns: 1

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


Requirements
------------

Prerequisites
~~~~~~~~~~~~~

Python 3.0

Generate API Key
~~~~~~~~~~~~~~~~

To use SDK, it requires you to `Generate API Key <https://developers.tune.com/management-docs/resource-authentication-user-permissions//>`_


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


Reporting Issues
----------------

We would love to hear your feedback.

Email: `sdk@tune.com <mailto:sdk@tune.com>`_

.. :changelog:

Release History
===============

2.2.1 (2017-10-27)
------------------
- Support logging-mv-integrations refactor

2.2.0 (2017-03-26)
------------------
- Replace 'json' with 'ujson'

2.1.8 (2017-03-12)
------------------
- Switch to using safe-cast package

2.1.7 (2017-02-27)
------------------
- Requirements

2.1.6 (2017-02-07)
------------------
- Requirements

2.1.5 (2017-02-03)
------------------
- Python 3.6 Upgrade

2.1.2 (2017-01-27)
------------------
- Cleanup
- Requirements

2.1.0 (2017-01-14)
------------------
- README.rst
- HISTORY.rst
- setup.py

2.0.0 (2016-11-20)
------------------
- TUNE Reporting API v3

1.1.1 (2016-01-25)
------------------
- TUNE Reporting API v2
- Changes in Handling Exports and Logs

1.0.0 (2015-04-01)
------------------
- TUNE Reporting API v2
- Initial PyPi release

0.0.1 (2014-10-15)
------------------
 - First Commit


