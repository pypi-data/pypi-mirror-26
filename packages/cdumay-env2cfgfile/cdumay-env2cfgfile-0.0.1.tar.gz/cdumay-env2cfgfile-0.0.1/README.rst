==================
cdumay-env2cfgfile
==================


.. image:: https://img.shields.io/pypi/v/cdumay-env2cfgfile.svg
   :target: https://pypi.python.org/pypi/cdumay-env2cfgfile/
   :alt: Latest Version

.. image:: https://travis-ci.org/cdumay/cdumay-env2cfgfile.svg?branch=master
   :target: https://travis-ci.org/cdumay/cdumay-env2cfgfile
   :alt: Latest version

A binary to dump environment into a file (Tested on python 2.7 & 3.5)

Quickstart
==========

First, install cdumay-env2cfgfile using `pip <https://pip.pypa.io/en/stable/>`_::

    pip install -U cdumay-env2cfgfile


Example
=======

The given example dump all environment QT variables in a json file::

    $ ./env2cfg --prefix 'QT_' json /tmp/myenv.json
    $ cat /tmp/myenv.json
    {
        "QT_ACCESSIBILITY": "1",
        "QT_IM_MODULE": "",
        "QT_LINUX_ACCESSIBILITY_ALWAYS_ON": "1",
        "QT_STYLE_OVERRIDE": "gtk"
    }

License
=======

MIT License