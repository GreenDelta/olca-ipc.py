olca-ipc.py
===========

openLCA provides an `implementation <https://github.com/GreenDelta/olca-modules/tree/master/olca-ipc>`_
of an `JSON-RPC <http://www.jsonrpc.org/specification>`_ based protocol for
inter-process communication (IPC). With this, it is possible to call functions
in openLCA and processing their results outside of openLCA. The ``olca-ipc``
package provides a convenience API for using this IPC protocol from standard
Python (Cpython v3.6+) so that it is possible to use openLCA as a data storage
and calculation engine and combine it with the libraries from the Python
ecosystem (numpy, pandas and friends).

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
calling functions of openLCA and processing their results. The following
examples show some typical uses cases.


**Create and link data**

The ``olca`` package contains a class model with type annotations for the
`olca-schema <https://github.com/GreenDelta/olca-schema>`_ model that is used
for exchanging data with openLCA. With the type annotations you should get good
editor support (type checks and IntelliSense). You can create, update
and link data models as defined in the openLCA schema (e.g. as for
`processes <http://greendelta.github.io/olca-schema/html/Process.html>`_,
`flows <http://greendelta.github.io/olca-schema/html/Flow.html>`_, or
`product systems <http://greendelta.github.io/olca-schema/html/ProductSystem.html>`_).

The ``olca.Client`` class provides methods like ``get``, ``find``, ``insert``,
``update``, and ``delete`` to work with data. The following example shows how to
create a new flow and link it to an existing flow property with the name `Mass`:


.. code-block:: python

    import olca
    import uuid

    client = olca.Client(8080)

    # find the flow property 'Mass' from the database
    mass = client.find(olca.FlowProperty, 'Mass')

    # create a flow that has 'Mass' as reference flow property
    steel = olca.Flow()
    steel.id = str(uuid.uuid4())
    steel.flow_type = olca.FlowType.PRODUCT_FLOW
    steel.name = "Steel"
    steel.description = "Added from the olca-ipc python API..."
    # in openLCA, conversion factors between different
    # properties/quantities of a flow are stored in
    # FlowPropertyFactor objects. Every flow needs at
    # least one flow property factor for its reference
    # flow property.
    mass_factor = olca.FlowPropertyFactor()
    mass_factor.conversion_factor = 1.0
    mass_factor.flow_property = mass
    mass_factor.reference_flow_property = True
    steel.flow_properties = [mass_factor]

    # save it in openLCA, you may have to refresh
    # (close & reopen the database to see the new flow)
    client.insert(steel)


For more information and examples see the
`package documentation <https://olca-ipc.readthedocs.io/en/latest/>`_
