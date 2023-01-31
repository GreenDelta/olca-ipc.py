
Monte-Carlo-Simulation is not defined yet for the new calculation queue:

```py
    def simulator(self, setup: results.CalculationSetup) -> schema.Ref:
        """
        Create a simulator to run Monte-Carlo simulations for the given setup.

        Parameters
        ----------

        setup: olca.schema.CalculationSetup
            The calculation setup that should be used.

        Returns
        -------

        olca.schema.Ref
            A reference to an simulator instance.

        Example
        -------
        ```python
        import olca

        client = olca.Client()
        # creating the calculation setup
        setup = olca.CalculationSetup()
        setup.impact_method = client.find(olca.ImpactMethod, 'TRACI [v2.1, February 2014]')
        setup.product_system = client.find(olca.ProductSystem, 'compost plant, open')
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
        ```
        """
        resp, err = self.rpc_call("simulator", setup.to_dict())
        if err:
            log.error("failed to create simulator: %s", err)
            return schema.Ref()
        return schema.Ref.from_dict(resp)

    def next_simulation(self, simulator: schema.Ref) -> schema.Result:
        """
        Runs the next Monte-Carlo simulation with the given simulator reference.
        It returns the result of the simulation. Note that this result is not
        cached (the simulator is cached).
        See [the simulator example](#olca.ipc.Client.simulator).

        Parameters
        ----------
        simulator: olca.schema.Ref
            The reference to the simulator which is called to run the next
            simulation step.

        """
        if simulator is None:
            raise ValueError("No simulator given")
        resp, err = self.rpc_call("next/simulation", simulator.to_dict())
        if err:
            log.error("failed to get simulation result: %s", err)
            return schema.Result()
        return schema.Result.from_dict(resp)
```

The old function for shutting down a sever should be removed?

```py
    def shutdown_server(self):
        """
        Close the database and shutdown the server.

        This method is probably most useful when running a headless server
        (a server without openLCA user interface).
        """
        _, err = self.rpc_call("runtime/shutdown", None)
        if err:
            log.error("failed to shutdown server: %s", err)
```

Better define an upstream tree that fetches data from the IPC protocol
instead of defining this in that protocol:

```py
    def upstream_tree_of(
        self,
        result: schema.Result,
        ref: schema.Ref,
        max_depth=5,
        min_contribution=0.1,
        max_recursion_depth=3,
    ) -> Optional[UpstreamTree]:
        """
        Get an upstream tree for an impact category or flow.

        This function is only available in openLCA 2.x.

        Parameters
        ----------
        result: olca.schema.SimpleResult
            The previously calculated result. This needs to be an upstream
            result.

        ref: olca.schema.Ref
            The result reference of the upstream tree: a flow or impact
            category reference.

        max_depth: int
            The maximum number of levels of the tree. A value < 0 means
            unlimited. In this case reasonable recursion limits are
            required if the underlying product system has cycles.

        min_contribution: float
            In addition to the maximum tree depth, this parameter describes
            the minimum upstream contribution of a node in the tree. A value
            < 0 means that there is no minimum contribution.

        max_recursion_depth: int
            When the max. tree depth is unlimited and the underlying product
            system has cycles, this parameter indicates how often a process
            can occur in a tree path. It defines the maximum number of
            expansions of a loop in a tree path.

        Example
        -------
        ```python
        client = olca.Client()

        # create the calculation setup and run the calculation
        setup = olca.CalculationSetup()
        setup.calculation_type = olca.CalculationType.UPSTREAM_ANALYSIS
        setup.product_system = olca.ref(
            olca.ProductSystem,
            '7d1cbce0-b5b3-47ba-95b5-014ab3c7f569'
        )
        setup.impact_method = olca.ref(
            olca.ImpactMethod,
            '99b9d86b-ec6f-4610-ba9f-68ebfe5691dd'
        )
        setup.amount = 1.0
        result = client.calculate(setup)

        # calculate the upstream tree and traverse it
        impact = olca.ref(
            olca.ImpactCategory,
            '2a26b243-23cb-4f90-baab-239d3d7397fa')
        tree = client.upstream_tree_of(result, impact)

        def traversal_handler(n: Tuple[UpstreamNode, int]):
            (node, depth) = n
            print('%s+ %s %.3f' % (
                '  ' * depth,
                node.product.process.name,
                node.result
            ))

        tree.traverse(traversal_handler)

        # dispose the result
        client.dispose(result)
        ```
        """
        raw, err = self.rpc_call(
            "get/upstream/tree",
            {
                "resultId": result.id,
                "ref": ref.to_dict(),
                "maxDepth": max_depth,
                "minContribution": min_contribution,
                "maxRecursionDepth": max_recursion_depth,
            },
        )
        if err:
            log.error("Failed to get upstream tree: %s", err)
            return None
        return UpstreamTree.from_dict(raw)
```

Signature for product system creation has changed:

```py
"""
        Creates a product system from the process with the given ID.

        Parameters
        ----------

        process_id: str
            The ID of the process from which the product system should be
            generated. This will be the reference process of the product system
            with upstream and downstream processes added recursively.

        default_providers: {'prefer', 'ignore', 'only'}, optional
            Indicates how default providers of product inputs and waste outputs
            should be considered during the linking. `only` means that only
            product inputs and waste outputs should be linked that have a
            default provider and that this default provider is used. `prefer`
            means that a default provider is used during the linking if there
            are multiple options. `ignore` means that the default providers
            have no specific role.

        preferred_type : {'LCI_RESULT', 'UNIT_PROCESS'}, optional
            When there are multiple provider processes available for linking a
            product input or waste output the `preferred_type` indicates which
            type of process (LCI results or unit processes) should be preferred
            during the linking.

        Returns
        -------

        olca.schema.Ref
            A descriptor of the created product system.

        Example
        -------

        ```python
        import olca

        client = olca.Client(8080)
        process_id = '4aee0b0c-eb46-37f1-8c7a-7e5b1adfd014'
        ref = client.create_product_system(process_id)
        print('Created product system %s' % ref.id)
        ```
        """
```

Removed Excel - Exports from the IPC protocol as this is out-of-scope:

```py
    def excel_export(self, result: schema.Result, path: str):
        """Export the given result to an Excel file with the given path.

        :param result: The result that should be exported.
        :param path: The path of the Excel file to which the result should be
                     written.
        """
        abs_path = os.path.abspath(path)
        params = {"@id": result.id, "path": abs_path}
        _, err = self.rpc_call("export/excel", params)
        if err:
            log.error("Excel export to %s failed: %s", path, err)
```

* result/demand
* get_direct_flows_of
  * ->

reate and link data
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

