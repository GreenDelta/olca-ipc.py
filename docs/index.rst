olca-ipc
========

openLCA provides an `implementation <https://github.com/GreenDelta/olca-modules/tree/master/olca-ipc>`_
of an `JSON-RPC <http://www.jsonrpc.org/specification>`_ based protocol for
inter-process communication (IPC). With this, it is possible to call functions
in openLCA and processing their results outside of openLCA. The ``olca-ipc``
package provides a convenience API for using this IPC protocol from standard
Python (Cpython v3.6+) so that it is possible to use openLCA as a data storage
and calculation engine and combine it with the libraries from the Python
ecosystem.

The openLCA IPC protocol is based on the openLCA data exchange format which is
specified in the `olca-schema <https://github.com/GreenDelta/olca-schema>`_
repository. The ``olca-ipc`` package provides a class based implementation of
the openLCA data exchange format and an API for communicating with an openLCA
IPC server via instances of these classes.

The current stable version of ``olca-ipc`` is available via the
`Python Package Index <https://pypi.org/project/olca-ipc/>`_. Thus, in order to
use it, you can just install (and uninstall) it with pip:

.. code-block:: bash

    pip install -U olca-ipc

In order to communicate with openLCA, you first need to start an openLCA IPC
server. You can do this via the user interface in openLCA under
``Window > Developer Tools > IPC Server``. The IPC server runs on a specific
port, e.g. ``8080``, to which you connect from an IPC client:

.. code-block:: python

    import olca
    client = olca.Client(8080)

An instance of the ``olca.Client`` class is then a convenient entry point for
calling functions of openLCA and processing their results.


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
