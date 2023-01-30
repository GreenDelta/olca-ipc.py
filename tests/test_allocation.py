import unittest

import olca_schema as lca
import olca_schema.units as units
import olca_schema.results as res

from config import client


class AllocationTest(unittest.TestCase):
    """
    Tests the calculation of results for different allocation methods.
    """

    def test_example(self):

        # get our quantity and unit, assuming that we are connected to an
        # openLCA database that contains these reference data
        mass = client.get(lca.FlowProperty, name="Mass")
        assert mass is not None
        kg = units.unit_ref("kg")
        assert kg is not None

        # create the flows p, q, e
        p = lca.new_product("p", mass)
        q = lca.new_product("q", mass)
        e = lca.new_elementary_flow("e", mass)
        for f in [p, q, e]:
            client.put(f)

        # create the process with inputs and outputs
        process = lca.new_process("P")
        assert process.id is not None
        lca.new_output(process, p, 1.0, kg).is_quantitative_reference = True
        lca.new_output(process, q, 1.0, kg)
        ex = lca.new_output(process, e, 1.0, kg)

        # define the allocation factors
        process.default_allocation_method = lca.AllocationType.CAUSAL_ALLOCATION
        lca.new_physical_allocation_factor(process, p, 0.25)
        lca.new_physical_allocation_factor(process, q, 0.75)
        lca.new_economic_allocation_factor(process, p, 0.4)
        lca.new_economic_allocation_factor(process, q, 0.6)
        lca.new_causal_allocation_factor(process, p, 0.1, ex)
        lca.new_causal_allocation_factor(process, q, 0.9, ex)

        # save the process and create the product system
        client.put(process)
        system = client.create_product_system(process)
        assert system is not None
        setup = res.CalculationSetup()
        setup.target = lca.Ref(model_type="ProductSystem", id=system.id)
        setup.amount = 500
        setup.unit = units.unit_ref("g")

        expected = [
            (lca.AllocationType.PHYSICAL_ALLOCATION, 0.25 / 2),
            (lca.AllocationType.ECONOMIC_ALLOCATION, 0.4 / 2),
            (lca.AllocationType.CAUSAL_ALLOCATION, 0.1 / 2),
            (lca.AllocationType.USE_DEFAULT_ALLOCATION, 0.1 / 2),
            (lca.AllocationType.NO_ALLOCATION, 0.5),
            (None, 0.5),
        ]
        for (method, value) in expected:
            print("test with allocation method = %s ..." % method)
            setup.allocation = method
            result = client.calculate(setup)
            result.wait_until_ready()
            # get the result for 'e'; when there is no allocation applied
            # we also have a result for ' q' in our list
            fr = next(
                r
                for r in result.get_total_flows()
                if r.envi_flow.flow.id == e.id
            )
            self.assertFalse(fr.envi_flow.is_input)
            self.assertAlmostEqual(value, fr.amount)
            result.dispose()
            print(" ... success")

        # set drop to False if you want to inspect the process in openLCA
        drop = False
        if drop:
            for each in (system, process, p, q, e):
                client.delete(each)


if __name__ == "__main__":
    unittest.main()
