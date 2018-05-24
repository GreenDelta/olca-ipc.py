olca-ipc.py
===========

``olca-ipc.py`` is a Python package for calling openLCA functions from
standard Python via inter-process communication... more doc will follow

Usage
-----
We will distribute the package later on PyPi; to install the current development
version just do: 

.. code:: bash

    pip install -e .

Running the tests:

.. code:: bash

    python -m unittest discover tests -v

Connecting with openLCA
~~~~~~~~~~~~~~~~~~~~~~~
In order to communicate with openLCA, you first need to start the openLCA
IPC server. You can do this via the user interface in openLCA under
``Window > Developer Tools > IPC Server``. The IPC server runs on a specific
port, e.g. ``8080``, to which you connect from an IPC client:

.. code-block:: python

    import olca
    client = olca.Client(8080)

An instance of the ``olca.Client`` class is then a convenient entry point for
calling functions of openLCA and processing their results.

Browsing the database content
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The method ``get_descriptors`` returns a list of data set references with some
meta-data for a given data set type (like ``olca.Flow``, ``òlca.Process``,
etc.):

.. code-block:: python

    methods = client.get_descriptors(olca.ImpactMethod)
    for method in methods:
        print('%s\t%s' % (method.id, method.name))


Insert, update, delete
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    actor = olca.Actor()
    actor.id = str(uuid.uuid4())
    actor.name = 'A test actor'
    resp = client.insert(actor)
    print(resp)  #  should print ' ok'


