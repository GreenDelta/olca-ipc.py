olca-ipc.py
===========

.. note::
    Not all features and bug-fixes are currently available on the version
    on PyPi.org. If you want to use the latest development version, just install
    it directly from the master branch, e.g. with ``pip``:

    ``pip install -U git+https://github.com/GreenDelta/olca-ipc.py.git/@master``

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

If you want to use the current development branch you can
`download it from Github <https://github.com/GreenDelta/olca-ipc.py/archive/master.zip>`_
and install it from the extracted folder:

.. code-block:: bash

    # optionally, first uninstall it
    # pip uninstall olca-ipc
    cd folder/where/you/extracted/the/zip
    pip install .

In order to communicate with openLCA, you first need to start an openLCA IPC
server. You can do this via the user interface in openLCA under
``Window > Developer Tools > IPC Server``. The IPC server runs on a specific
port, e.g. ``8080``, to which you connect from an IPC client:

.. code-block:: python

    import olca
    client = olca.Client(8080)

An instance of the ``olca.Client`` class is then a convenient entry point for
calling functions of openLCA and processing their results. The following
examples show some typical uses cases (note that these are just examples
without input checks, error handling, code structuring, and all the things you
would normally do).


Create and link data
~~~~~~~~~~~~~~~~~~~~

The ``olca`` package contains a class model with type annotations for the
`olca-schema <https://github.com/GreenDelta/olca-schema>`_ model that is used
for exchanging data with openLCA. With the type annotations you should get good
editor support (type checks and IntelliSense). You can create, update
and link data models as defined in the openLCA schema (e.g. as for
`processes <http://greendelta.github.io/olca-schema/html/Process.html>`_,
`flows <http://greendelta.github.io/olca-schema/html/Flow.html>`_, or
`product systems <http://greendelta.github.io/olca-schema/html/ProductSystem.html>`_).
(Note that we convert camelCase names like ``calculationType`` of attributes and
functions to lower_case_names_with_underscores like ``calculation_type`` when
generating the Python API).

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


Running calculations
~~~~~~~~~~~~~~~~~~~~

openLCA provides different types of calculations which can be selected via the
``calculation_type`` in a
`calculation setup <http://greendelta.github.io/olca-schema/html/CalculationSetup.html>`_.
In the following example, a calculation setup with a product system and impact
assessment method is created, calculated, and finally exported to Excel:


.. code-block:: python

    import olca

    client = olca.Client(8080)

    # create the calculation setup
    setup = olca.CalculationSetup()

    # define the calculation type here
    # see http://greendelta.github.io/olca-schema/html/CalculationType.html
    setup.calculation_type = olca.CalculationType.CONTRIBUTION_ANALYSIS

    # select the product system and LCIA method
    setup.impact_method = client.find(olca.ImpactMethod, 'TRACI 2.1')
    setup.product_system = client.find(olca.ProductSystem, 'compost plant, open')

    # amount is the amount of the functional unit (fu) of the system that
    # should be used in the calculation; unit, flow property, etc. of the fu
    # can be also defined; by default openLCA will take the settings of the
    # reference flow of the product system
    setup.amount = 1.0

    # calculate the result and export it to an Excel file
    result = client.calculate(setup)
    client.excel_export(result, 'result.xlsx')

    # the result remains accessible (for exports etc.) until
    # you dispose it, which you should always do when you do
    # not need it anymore
    client.dispose(result)


Parameterized calculation setups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In order to calculate a product system with different parameter sets, you can
pass a set of parameter redefinitions directly with a calculation setup into
a calculation. With this, you do not need to modify a product system or the
parameters in a database in order to calculate it with different parameter
values:

.. code-block:: python

    # ... same steps as above
    setup = olca.CalculationSetup()
    # ...
    for something in your.parameter_data:
        redef = olca.ParameterRedef()
        redef.name = the_parameter_name
        redef.value = the_parameter_value
        # redef.context = ... you can also redefine process and LCIA method
        #                     parameters by providing a parameter context which
        #                     is a Ref (reference) to the respective process or
        #                     LCIA method; with no context a global parameter is
        #                     redefined
        setup.parameter_redefs.append(redef)


As the name says, a parameter redefinition redefines the value of an existing
global, process, or LCIA method parameter.


Monte-Carlo simulations
~~~~~~~~~~~~~~~~~~~~~~~
Running Monte-Carlo simulations is similar to normal calculations but instead
of ``calculate`` you call the ``simulator`` method which will return a reference
to a simulator which you then use to run calculations (where in each calculation
the simulator generates new values for the uncertainty distributions in the
system). You get the result for each iteration and can also export the result of
all iterations later to Excel. As for the results of the normal calculation, the
the simulator should be disposed when it is not used anymore:


.. code-block:: python

    import olca

    client = olca.Client(8080)

    # creating the calculation setup
    setup = olca.CalculationSetup()
    setup.calculation_type = olca.CalculationType.MONTE_CARLO_SIMULATION
    setup.impact_method = client.find(olca.ImpactMethod, 'TRACI 2.1')
    setup.product_system = client.find(olca.ProductSystem, 'compost plant')
    setup.amount = 1.0

    # create the simulator
    simulator = client.simulator(setup)

    for i in range(0, 10):
        result = client.next_simulation(simulator)
        first_impact = result.impact_results[0]
        print('iteration %i: result for %s = %4.4f' %
              (i, first_impact.impact_category.name, first_impact.value))
        # we do not have to dispose the result here (it is not cached
        # in openLCA); but we need to dispose the simulator later (see below)

    # export the complete result of all simulations
    client.excel_export(simulator, 'simulation_result.xlsx')

    # the result remains accessible (for exports etc.) until
    # you dispose it, which you should always do when you do
    # not need it anymore
    client.dispose(simulator)


For more information and examples see the
`package documentation <https://greendelta.github.io/olca-ipc.py/olca/>`_
