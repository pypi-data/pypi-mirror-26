========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-file/badge/?style=flat
    :target: https://readthedocs.org/projects/python-file
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/ionelmc/python-file.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/ionelmc/python-file

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/ionelmc/python-file?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/ionelmc/python-file

.. |requires| image:: https://requires.io/github/ionelmc/python-file/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/ionelmc/python-file/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/ionelmc/python-file/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/ionelmc/python-file

.. |codecov| image:: https://codecov.io/github/ionelmc/python-file/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/ionelmc/python-file

.. |version| image:: https://img.shields.io/pypi/v/file.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/file

.. |commits-since| image:: https://img.shields.io/github/commits-since/ionelmc/python-file/v0.3.0.svg
    :alt: Commits since latest release
    :target: https://github.com/ionelmc/python-file/compare/v0.3.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/file.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/file

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/file.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/file

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/file.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/file


.. end-badges

CFFI bindings for libmagic.

* Free software: MIT License

Installation
============

::

    pip install file

Usage
=====

.. code-block:: python

    from file import Magic

    with Magic() as magic:
        print(magic.buffer("hello")) # => "text/plain"

    from file import magic_buffer, magic_file, magic_setflags

    magic = Magic()
    mimetype = magic_buffer("\x89\x50\x4E\x47\x0D\x0A\x1A\x0A")
    print(mimetype) # => "image/png"

    mimetype = magic_file("/etc/passwd")
    print(mimetype) # => "text/plain"

    from file import MAGIC_NONE
    magic_setflags(MAGIC_NONE)
    mimetype = magic_file("demo.docx")
    print(mimetype) # => "Microsoft Word 2007+"
    magic.close() # don't forget about this
