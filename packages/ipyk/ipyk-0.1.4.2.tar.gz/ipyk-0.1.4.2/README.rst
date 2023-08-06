.. -*- rst -*-

IPyk
====

Package Description
-------------------
IPyk is a command line utility for managing locally run IPython kernels.

.. image:: https://img.shields.io/pypi/v/ipyk.svg
    :target: https://pypi.python.org/pypi/ipyk
    :alt: Latest Version

Installation
------------
If you have `pip <http://www.pip-installer.org/>`_ installed, run::
  
    pip install ipyk

You can also download the source tarball, unpack, and run::

    python setup.py install

Usage
-----
Start a new kernel using the default IPython profile: ::
    
    ipyk -s

Start a new kernel using a specific profile: ::

    ipyk -s my_profile

List running kernels; depending on the version of IPython you are using, the 
kernel JSON files may be stored in different locations: ::

    ipyk -l
    0: /run/user/1000/jupyter/kernel-12345.json

Connect to a running kernel; note that the argument is the integer listed by 
``ipyk -l``, not the process ID: ::

    ipyk -c 0

After connecting to a running kernel, one can disconnect without killing the 
kernel by running ``quit(keep_kernel=True)``.

Terminate a running kernel: ::

    ipyk -k 0

Author
------
See the included `AUTHORS.rst
<https://github.com/lebedov/ipyk/blob/master/AUTHORS.rst>`_ file for more
information.


License
-------
This software is licensed under the `BSD License
<http://www.opensource.org/licenses/bsd-license>`_.  See the included
`LICENSE.rst <https://github.com/lebedov/ipyk/blob/master/LICENSE.rst>`_ file
for more information.
