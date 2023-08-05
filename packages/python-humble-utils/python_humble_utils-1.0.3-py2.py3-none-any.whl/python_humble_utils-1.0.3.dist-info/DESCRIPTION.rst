Python Humble Utils
===================

.. image:: https://travis-ci.org/webyneter/python-humble-utils.svg?branch=master
    :target: https://travis-ci.org/webyneter/python-humble-utils
    :alt: Build Status

.. image:: https://pyup.io/repos/github/webyneter/python-humble-utils/shield.svg
    :target: https://pyup.io/repos/github/webyneter/python-humble-utils
    :alt: Updates

.. image:: https://codecov.io/gh/webyneter/python-humble-utils/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/webyneter/python-humble-utils
    :alt: Coverage

.. image:: https://codeclimate.com/github/webyneter/python-humble-utils/badges/gpa.svg
    :target: https://codeclimate.com/github/webyneter/python-humble-utils
    :alt: Code Climate

.. image:: https://badge.fury.io/py/python-humble-utils.svg
    :target: https://pypi.python.org/pypi/python-humble-utils
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/python-humble-utils.svg
    :target: https://pypi.python.org/pypi/python-humble-utils
    :alt: Supported Python Versions

.. image:: https://readthedocs.org/projects/python-humble-utils/badge/?version=stable
    :target: http://python-humble-utils.readthedocs.io/en/stable/?badge=stable
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-MIT-green.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

.. image:: https://img.shields.io/gitter/room/webyneter/python-humble-utils.svg
    :target: https://gitter.im/webyneter/python-humble-utils?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
    :alt: Join the chat at https://gitter.im/webyneter/python-humble-utils


Python utils for everyday use.

* `Documentation`_.
* Please, `open issues`_ before sending emails to the maintainers: You will get a much faster response!

.. _`open issues`: https://github.com/webyneter/python-humble-utils/issues/new
.. _`Documentation`: https://python-humble-utils.readthedocs.io/en/stable/



Feature Areas
-------------

* File operations.
* File/directory paths extraction.
* File/directory paths randomization.
* String case conversions.
* Python class convenience shortcuts.
* `py.test`_ fixtures and helpers.

.. _`py.test`: https://docs.pytest.org/en/stable/



Installation
------------

.. code-block:: console

    $ pip install python-humble-utils

or install from sources:

.. code-block:: console

    $ python setup.py install

Refer to `Installation`_ for detailed instructions.

.. _`Installation`: https://python-humble-utils.readthedocs.io/en/stable/installation.html


Usage
-----

.. code-block:: python

    import os

    from python_humble_utils.commands import (
        yield_file_paths,
        camel_or_pascal_case_to_snake_case
    )


    # ...


    file_paths = yield_file_paths(dir_path=os.path.join('dir', 'with', 'scripts'),
                                  allowed_file_extensions=['.sh', '.bash'],
                                  recursively=True)
    # assert set(file_paths) == set(['s1.sh', 's2.bash', 's3.bash'])

    s = camel_or_pascal_case_to_snake_case('camelCasedString')
    # assert s == 'camel_cased_string'

    s = camel_or_pascal_case_to_snake_case('PascalCasedString')
    # assert s == 'pascal_cased_string'


    # ...


Contributing
------------

Your contributions are very much welcome! Refer to `Contributing`_ for more details.

.. _`Contributing`: https://python-humble-utils.readthedocs.io/en/stable/contributing.html



Code of Conduct
---------------

All those using ``python-humble-utils``, including its codebase and project management ecosystem are expected to follow the `Python Community Code of Conduct`_.

.. _`Python Community Code of Conduct`: https://www.python.org/psf/codeofconduct/



Acknowledgements
----------------

This package was scaffolded via `Cookiecutter`_ with `audreyr/cookiecutter-pypackage`_ template.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



History
=======


v1.0.2
------

`v1.0.2 <https://github.com/webyneter/python-humble-utils/releases/tag/v1.0.2>`_.

* `Add Code Climate badge to README <https://github.com/webyneter/python-humble-utils/issues/45>`_.


v1.0.1
------

`v1.0.1 <https://github.com/webyneter/python-humble-utils/releases/tag/v1.0.1>`_.

* `Fix README not rendered properly on PyPI <https://github.com/webyneter/python-humble-utils/issues/43>`_.


v1.0.0
------

`v1.0.0 <https://github.com/webyneter/python-humble-utils/releases/tag/v1.0.0>`_.

* `Bump package Development Status <https://github.com/webyneter/python-humble-utils/issues/18>`_.
* `Test package deployment locally <https://github.com/webyneter/python-humble-utils/issues/11>`_.
* `Fix relative paths notice <https://github.com/webyneter/python-humble-utils/issues/38>`_.
* `Add Gitter badge <https://github.com/webyneter/python-humble-utils/issues/20>`_.
* `Fill in HISTORY <https://github.com/webyneter/python-humble-utils/issues/35>`_.


v0.5.0
------

`v0.5.0 <https://github.com/webyneter/python-humble-utils/releases/tag/v0.5.0>`_.

* `Document python_humble_utils package <https://github.com/webyneter/python-humble-utils/issues/28>`_.
* `Introduce local requirements <https://github.com/webyneter/python-humble-utils/issues/15>`_.
* `Stop using pip-tools <https://github.com/webyneter/python-humble-utils/issues/29>`_.
* `Point out that all paths in docs are relative to the project root <https://github.com/webyneter/python-humble-utils/issues/30>`_.
* `Prevent pip-tools from injecting indirect requirements <https://github.com/webyneter/python-humble-utils/issues/14>`_.
* `Target stable docs version only <https://github.com/webyneter/python-humble-utils/issues/22>`_.
* `Fix README not rendered on PyPI <https://github.com/webyneter/python-humble-utils/issues/17>`_.
* `Ensure codecov evaluates coverage against payload files only <https://github.com/webyneter/python-humble-utils/issues/21>`_.


v0.4.0
------

`v0.4.0 <https://github.com/webyneter/python-humble-utils/releases/tag/v0.4.0>`_.

* `Support Python 3.6 <https://github.com/webyneter/python-humble-utils/issues/4>`_.


v0.3.0
------

`v0.3.0 <https://github.com/webyneter/python-humble-utils/releases/tag/v0.3.0>`_.

* `Setup ReadTheDocs <https://github.com/webyneter/python-humble-utils/issues/10>`_.


v0.2.0
------

`v0.2.0 <https://github.com/webyneter/python-humble-utils/releases/tag/v0.2.0>`_.

* First release on PyPI.


