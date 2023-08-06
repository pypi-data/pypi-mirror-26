.. -*- mode: rst -*-

logging-mv-integrations
-----------------------

Python logging library for TUNE Multiverse Integrations.


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


.. |docs| image:: https://readthedocs.org/projects/logging-mv-integrations/badge/?style=flat
    :alt: Documentation Status
    :target: https://readthedocs.org/projects/logging-mv-integrations

.. |license| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :alt: License Status
    :target: https://opensource.org/licenses/MIT

.. |travis| image:: https://travis-ci.org/TuneLab/logging-mv-integrations.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/TuneLab/logging-mv-integrations

.. |coveralls| image:: https://coveralls.io/repos/TuneLab/logging-mv-integrations/badge.svg?branch=master&service=github
    :alt: Code Coverage Status
    :target: https://coveralls.io/r/TuneLab/logging-mv-integrations

.. |requires| image:: https://requires.io/github/TuneLab/logging-mv-integrations/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/TuneLab/logging-mv-integrations/requirements/?branch=master

.. |version| image:: https://img.shields.io/pypi/v/logging_mv_integrations.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/logging_mv_integrations

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/tune_reporting.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/tune_reporting

.. end-badges


Install
-------

.. code-block:: bash

    pip install logging_mv_integrations

UML
---

``logging-mv-integrations`` is a Python logging library for TUNE Multiverse Integrations.

.. image:: ./images/logging_mv_integrations.png
   :scale: 50 %
   :alt: UML logging-mv-integrations


Function: get_logger()
----------------------

.. code-block:: python

    def get_logger(
        logger_name,
        logger_version=None,
        logger_level=logging.INFO,
        logger_format=LoggingFormat.JSON,
        logger_output=LoggingOutput.STDOUT_COLOR,
        logger_handler=None
    ):


.. :changelog:

Release History
===============

0.1.8 (2017-11-21)
------------------
- README

0.1.7 (2017-10-26)
------------------
- Using Formatted String Literals

0.1.6 (2017-10-19)
------------------
- Logging Output: FILE, STDOUT, STDOUT_COLOR

0.1.5 (2017-10-17)
------------------
- Fix standard format

0.1.4 (2017-10-09)
------------------
- Multiple handlers fix

0.1.3 (2017-09-12)
------------------
- Use python standard logging instead of tune_logging and remove all unneeded files

0.1.2 (2017-02-03)
------------------
- Switch to using casting from safe-cast package

0.1.1 (2017-02-03)
------------------
- Python 3.6 Upgrade

0.0.1 (2016-11-19)
------------------
 - First Commit

