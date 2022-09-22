import unittest

import olca as ipc
import olca_schema as lca
import olca_schema.units as units


class AllocationTest(unittest.TestCase):
    """
    Tests the calculation of results for different allocation
    methods. Note that this test uses functions that are only
    available in openLCA 2.x and, thus, do not work with
    openLCA 1.x.
    """

    def test_example(self):
        client = ipc.Client()

        # get our quantity and unit, assuming that we are
        # connected to an openLCA database that contains
        # these reference data and that there are not
        # multiple flow properties or units with the
        # name 'Mass' or ' kg' in this database
        mass = client.get(lca.FlowProperty, name='Mass')
        kg = units.unit_ref('kg')
        self.assertIsNotNone(mass)
        self.assertIsNotNone(kg)

        # create some flows
        p = lca.new_product('p', mass)
        q = lca.new_product('q', mass)
        e = lca.new_elementary_flow('e', mass)
        for f in [p, q, e]:
            client.insert(f)

        # create a process with inputs and outputs
        process = lca.new_process('P')
        lca.new_output(process, p, 1.0, kg) \
            .quantitative_reference = True
        lca.new_output(process, q, 1.0, kg)
        ex = lca.new_output(process, e, 1.0, kg)

        # define some allocation factors
        process.default_allocation_method = \
            lca.AllocationType.CAUSAL_ALLOCATION
        lca.new_physical_allocation_factor(process, p, 0.25)
        lca.new_physical_allocation_factor(process, q, 0.75)
        lca.new_economic_allocation_factor(process, p, 0.4)
        lca.new_economic_allocation_factor(process, q, 0.6)
        lca.new_causal_allocation_factor(process, p, 0.1, ex)
        lca.new_causal_allocation_factor(process, q, 0.9, ex)

        # save the process and create the product system
        client.insert(process)
        system = client.create_product_system(process.id)
        setup = ipc.CalculationSetup()
        setup.product_system = system
        setup.amount = 500
        setup.unit = units.unit_ref('g')

        expected = [
            (lca.AllocationType.PHYSICAL_ALLOCATION, 0.125),
            (lca.AllocationType.ECONOMIC_ALLOCATION, 0.2),
            (lca.AllocationType.CAUSAL_ALLOCATION, 0.05),
            (lca.AllocationType.USE_DEFAULT_ALLOCATION, 0.05),
            (lca.AllocationType.NO_ALLOCATION, 0.5),
            (None, 0.5),
        ]
        for (method, value) in expected:
            print('test with allocation method = %s ...' % method)
            setup.allocation_method = method
            result = client.calculate(setup)
            # get the result for 'e'; when there is no allocation applied
            # we also have a result for ' q' in our list
            fr = next(r for r in result.flow_results if r.flow.id == e.id)
            self.assertFalse(fr.input)
            self.assertAlmostEqual(value, fr.value)
            client.dispose(result)
            print(' ... success')

        # set drop to False if you want to inspect the process in openLCA
        drop = False
        if drop:
            for each in (system, process, p, q, e):
                client.delete(each)
