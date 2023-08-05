========
Overview
========

pyGAPS (Python General Adsorption Processing Suite) is a framework for adsorption data analysis written in python 3.




Features
========

    - Routine analysis such as BET surface area, t-plot, alpha-s method
    - Pore size distribution calculations for mesopores (BJH, Dollimore-Heal)
    - Pore size distribution calculations for micropores (Horvath-Kawazoe)
    - Pore size distribution calculations using DFT kernels
    - Isotherm modelling (Henry, Langmuir, DS/TS Langmuir, etc..)
    - IAST predictions for binary adsorption
    - Isosteric heat of adsorption calculation
    - Parsing to and from multiple formats such as Excel, CSV and JSON
    - An sqlite database backend for storing and retrieving data
    - Simple methods for isotherm graphing and comparison

Documentation
=============

For more info, as well as a complete manual and reference visit:

https://pygaps.readthedocs.io/

Most of the examples in the documentation are actually in the form of Jupyter Notebooks
which are turned into webpages with nbsphinx. You can find them for download in:

https://github.com/pauliacomi/pyGAPS/tree/master/docs/examples


Installation
============

The easiest way to install pyGAPS is from the command line.

.. code-block:: bash

    pip install pygaps

On Windows, `Anaconda/Conda <https://www.anaconda.com/>`__ is your best bet since it manages
environments for you.
First install the suite and then use pip inside your regular python 3 environment.

Alternatively, to install the development branch, clone the repository from Github.
Then install the package with setuptools, either in regular or developer mode

.. code-block:: bash

    git clone https://github.com/pauliacomi/pyGAPS

    # then install

    setup.py install

    # or developer mode

    setup.py develop

Development
===========

If you have all the python environments needed to run the entire test suite,
use tox. To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

For testing only with the environment you are currently on, run pytest instead::

    py.test --cov

Alternatively, you can depend on travisCI for the testing, which will be slower overall
but should have all the environments required.

Questions?
==========

I'm more than happy to answer any questions. Shoot me an email at paul.iacomi@univ-amu or find
me on some social media.

For any bugs found, please open an `issue <https://github.com/pauliacomi/pyGAPS/issues/>`__ or, If
you feel like you can do the fix yourself, submit a `pull request <https://github.com/pauliacomi/pyGAPS/pulls/>`__.
It'll make my life easier

This also applies to any features which you think might benefit the project.


Changelog
=========

0.9.1 (2017-10-23)
------------------

* Better examples
* Small fixes and improvements

0.9.0 (2017-10-20)
------------------

* Code is now in mostly working state.
* Manual and reference are built.


0.1.0 (2017-07-27)
------------------

* First release on PyPI.


