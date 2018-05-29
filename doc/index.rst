olca-ipc.py
===========

openLCA provides an `implementation <https://github.com/GreenDelta/olca-modules/tree/master/olca-ipc>`_
of an `JSON-RPC <http://www.jsonrpc.org/specification>`_ based protocol for
inter-process communication (IPC). With this, it is possible to call functions
in openLCA and processing their results outside of openLCA. The ``olca-ipc.py``
package provides a convenience API for using this IPC protocol from standard
Python (Cpython v3.4+) so that it is possible to use openLCA as a data storage
and calculation engine and combine it with the libraries from the Python
ecosystem.

The openLCA IPC protocol is based on the openLCA data exchange format which is
specified in the `olca-schema <https://github.com/GreenDelta/olca-schema>`_
repository. The ``olca-ipc.py`` package provides a class based implementation of
the openLCA data exchange format and an API for communicating with an openLCA
IPC server via instances of these classes.

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    example
    modules

Indices and tables
~~~~~~~~~~~~~~~~~~

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
