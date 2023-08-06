.. image:: https://travis-ci.org/alanhamlett/pip-update-requirements.svg?branch=master
    :target: https://travis-ci.org/alanhamlett/pip-update-requirements
    :alt: Tests

.. image:: https://coveralls.io/repos/alanhamlett/pip-update-requirements/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/alanhamlett/pip-update-requirements?branch=master
    :alt: Coverage

.. image:: https://gemnasium.com/badges/github.com/alanhamlett/pip-update-requirements.svg
    :target: https://gemnasium.com/github.com/alanhamlett/pip-update-requirements
    :alt: Dependencies

.. image:: https://badge.fury.io/py/pur.svg
    :target: https://pypi.python.org/pypi/pur
    :alt: Version


pip-update-requirements
=======================

Update the packages in a ``requirements.txt`` file.

.. image:: https://raw.githubusercontent.com/alanhamlett/pip-update-requirements/master/pur.gif
    :alt: Purring Cat


Installation
------------

::

    pip install pur


Usage
-----

Give pur your ``requirements.txt`` file and it updates all your packages to
the latest versions.

For example, given a ``requirements.txt`` file::

    flask==0.9
    sqlalchemy==0.9.10
    alembic==0.8.4

Running pur on that file updates the packages to current latest versions::

    $ pur -r requirements.txt
    Updated flask: 0.9 -> 0.10.1
    Updated sqlalchemy: 0.9.10 -> 1.0.12
    Updated alembic: 0.8.4 -> 0.8.6
    All requirements up-to-date.


Pur never modifies your environment or installed packages, it only modifies
your ``requirements.txt`` file.


Options
-------

-r, --requirement PATH   The requirements.txt file to update; Defaults to
                         using requirements.txt from the current directory
                         if it exist.
-o, --output PATH        Output updated packages to this file; Defaults to
                         overwriting the input requirements.txt file.
-i, --interactive        Interactively prompts before updating each package.
-f, --force              Force updating packages even when a package has no
                         version specified in the input requirements.txt
                         file.
-d, --dry-run            Output changes to STDOUT instead of overwriting the
                         requirements.txt file.
-n, --no-recursive       Prevents updating nested requirements files.
-s, --skip TEXT          Comma separated list of packages to skip updating.
--only TEXT              Comma separated list of packages. Only these
                         packages will be updated.
-z, --nonzero-exit-code  Exit with status l0 when all packages up-to-date,
                         11 when some packages were updated. Defaults to
                         exit status zero on success and non-zero on
                         failure.
--version                Show the version and exit.
--help                   Show this message and exit.


Contributing
------------

Before contributing a pull request, make sure tests pass::

    virtualenv venv
    . venv/bin/activate
    pip install tox
    tox

Many thanks to all `contributors <https://github.com/alanhamlett/pip-update-requirements/blob/master/AUTHORS>`_!
