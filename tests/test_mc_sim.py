import unittest
import statistics as stats

import olca_schema as o
from config import client


class MCSimTest(unittest.TestCase):
    def test_sim(self):

        # create units and flows
        units = o.new_unit_group("Units of mass", "kg")
        mass = o.new_flow_property("Mass", units)
        p = o.new_product("p", mass)
        q = o.new_product("q", mass)
        e = o.new_elementary_flow("e", mass)

        # create the process
        process = o.new_process("P")
        qref = o.new_output(process, p, amount=0.5)
        qref.is_quantitative_reference = True
        o.new_output(process, q, amount=0.5)
        o.new_output(process, e, amount=2).uncertainty = o.Uncertainty(
            distribution_type=o.UncertaintyType.NORMAL_DISTRIBUTION,
            mean=2,
            sd=0.1,
        )
        o.new_physical_allocation_factor(process, p, 0.2)
        o.new_physical_allocation_factor(process, q, 0.8)

        # create the LCIA indicator and method
        i = o.new_impact_category("i")
        o.new_impact_factor(i, e, value=2)
        method = o.new_impact_method("M", i)

        client.put_all(units, mass, p, q, e, process, i, method)

        setup = o.CalculationSetup(
            allocation=o.AllocationType.PHYSICAL_ALLOCATION,
            target=o.as_ref(process),
            amount=1,
            impact_method=o.as_ref(method),
        )

        # run simulations and collect indicator results
        xs = []
        result = client.simulate(setup)

        def put_next():
            result.wait_until_ready()
            xi = result.get_total_impact_value_of(o.as_ref(i))
            xs.append(xi.amount)

        put_next()
        for _ in range(0, 9):
            result.simulate_next()
            put_next()

        mean = stats.mean(xs)
        self.assertAlmostEqual(1.6, mean, delta=0.4)
        # print(xs)

        # clean up
        result.dispose()
        client.delete_all(method, i, process, e, p, q, mass, units)


if __name__ == "__main__":
    unittest.main()
