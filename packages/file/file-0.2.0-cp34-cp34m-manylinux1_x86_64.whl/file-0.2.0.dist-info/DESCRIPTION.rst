========
Overview
========



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


Changelog
=========

0.1.0 (2017-11-02)
------------------

* First release on PyPI.


