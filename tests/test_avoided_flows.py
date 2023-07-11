import unittest

import olca_schema as o

from config import client


class AvoidedFlowTest(unittest.TestCase):
    def setUp(self):
        units = o.new_unit_group("Units of mass", "kg")
        mass = o.new_flow_property("Mass", units)
        e = o.new_elementary_flow("e", mass)
        p = o.new_product("p", mass)
        q = o.new_product("q", mass)
        w = o.new_waste("w", mass)

        P = o.new_process("P")
        o.new_output(P, p, amount=1).is_quantitative_reference = True
        o.new_output(P, e, amount=1)

        W = o.new_process("W")
        o.new_input(W, w, amount=1).is_quantitative_reference = True
        o.new_output(W, e, amount=1)

        # P ->\ Q ->\ W
        Q = o.new_process("Q")
        o.new_output(Q, q, amount=1).is_quantitative_reference = True
        avoided_p = o.new_input(Q, p, amount=1)
        avoided_p.is_avoided_product = True
        avoided_p.default_provider = P.to_ref()
        avoided_w = o.new_output(Q, w, amount=1)
        avoided_w.is_avoided_product = True
        avoided_w.default_provider = W.to_ref()

        client.put_all(units, mass, e, p, q, w, P, W, Q)
        self.entities = [units, mass, e, p, q, w, P, W, Q]
        self.Q = Q

    def tearDown(self):
        client.delete_all(*self.entities)

    def test_calculation(self):
        setup = o.CalculationSetup(target=self.Q.to_ref())
        result = client.calculate(setup)
        result.wait_until_ready()
        e = next(
            filter(
                lambda ei: ei.envi_flow.flow.name == "e",
                result.get_total_flows(),
            )
        )
        self.assertAlmostEqual(-2, e.amount)
        result.dispose()


if __name__ == "__main__":
    unittest.main()
