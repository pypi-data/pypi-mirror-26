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
