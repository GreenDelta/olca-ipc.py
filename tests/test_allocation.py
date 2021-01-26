import unittest

import olca


class AllocationTest(unittest.TestCase):
    """
    Tests the calculation of results for different allocation
    methods. Note that this test uses functions that are only
    available in openLCA 2.x and, thus, do not work with
    openLCA 1.x.
    """

    def test_example(self):
        client = olca.Client()

        # get our quantity and unit, assuming that we are
        # connected to an openLCA database that contains
        # these reference data and that there are not
        # multiple flow properties or units with the
        # name 'Mass' or ' kg' in this database
        mass = client.get(olca.FlowProperty, name='Mass')
        kg = client.get(olca.Unit, name='kg')
        self.assertIsNotNone(mass)
        self.assertIsNotNone(kg)

        # create some flows
        p = olca.product_flow_of('p', mass)
        q = olca.product_flow_of('q', mass)
        e = olca.elementary_flow_of('e', mass)
        for f in [p, q, e]:
            client.insert(f)

        # create a process with inputs and outputs
        process = olca.process_of('P')
        olca.output_of(process, p, 1.0, kg) \
            .quantitative_reference = True
        olca.output_of(process, q, 1.0, kg)
        ex = olca.output_of(process, e, 1.0, kg)

        # define some allocation factors
        process.default_allocation_method = \
            olca.AllocationType.CAUSAL_ALLOCATION
        olca.physical_allocation_of(process, p, 0.25)
        olca.physical_allocation_of(process, q, 0.75)
        olca.economic_allocation_of(process, p, 0.4)
        olca.economic_allocation_of(process, q, 0.6)
        olca.causal_allocation_of(process, p, 0.1, ex)
        olca.causal_allocation_of(process, q, 0.9, ex)

        # save the process and create the product system
        client.insert(process)
        system = client.create_product_system(process.id)
        setup = olca.CalculationSetup()
        setup.product_system = system
        setup.amount = 500
        setup.unit = client.get_descriptor(olca.Unit, name='g')

        expected = [
            (olca.AllocationType.PHYSICAL_ALLOCATION, 0.125),
            (olca.AllocationType.ECONOMIC_ALLOCATION, 0.2),
            (olca.AllocationType.CAUSAL_ALLOCATION, 0.05),
            (olca.AllocationType.USE_DEFAULT_ALLOCATION, 0.05),
            (olca.AllocationType.NO_ALLOCATION, 0.5),
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
        drop = True
        if drop:
            for each in (system, process, p, q, e):
                client.delete(each)
