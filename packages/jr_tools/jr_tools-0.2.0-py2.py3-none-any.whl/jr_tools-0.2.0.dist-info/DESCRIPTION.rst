===================
JasperReports Tools
===================


.. image:: https://img.shields.io/pypi/v/jr_tools.svg
        :target: https://pypi.python.org/pypi/jr_tools

.. image:: https://img.shields.io/travis/erickgnavar/jasper-reports-tools.svg
        :target: https://travis-ci.org/erickgnavar/jasper-reports-tools

.. image:: https://readthedocs.org/projects/jasperreports-tools/badge/?version=latest
        :target: https://jasperreports-tools.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/erickgnavar/jr_tools/shield.svg
     :target: https://pyup.io/repos/github/erickgnavar/jr_tools/
     :alt: Updates


A collection of tools to handle Jasper Reports with python


* Free software: MIT license
* Documentation: http://jasperreports-tools.readthedocs.io.

Tested with JasperServer CE 6.4


Features
--------

* Client to get reports in API available formats(PDF, xls, etc)
* CLI: run ``jr_tools --help`` to get the list of available commands
* CLI: load resources from yaml file ``jr_tools load path_to_yaml_file``


TODO
----
* Django helper to consume reports and converto to Django responses


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


=======
History
=======

0.2.0 (2017-10-31)
------------------

* Add suport to upload and configure files and reports to JasperServer using a yml file

0.1.0 (2017-07-30)
------------------

* First release on PyPI.


