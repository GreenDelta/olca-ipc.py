import unittest

import olca_schema as o
import olca_ipc.utree as utree

from config import client


class TestUpstreamTree(unittest.TestCase):
    def test_upstream_tree(self):
        units = o.new_unit_group("Units of mass", "kg")
        mass = o.new_flow_property("Mass", units)
        e = o.new_elementary_flow("e", mass)
        p = o.new_product("p", mass)
        q = o.new_product("q", mass)

        P = o.new_process("P")
        Q = o.new_process("Q")
        o.new_output(P, p, amount=1).is_quantitative_reference = True
        o.new_input(P, q, amount=1).default_provider = Q.to_ref()
        o.new_output(P, e, amount=2)
        o.new_output(Q, q, amount=1).is_quantitative_reference = True
        o.new_input(Q, p, amount=0.5).default_provider = P.to_ref()
        o.new_output(Q, e, amount=4)

        client.put_all(units, mass, e, p, q, P, Q)

        setup = o.CalculationSetup(
            target=o.Ref(ref_type=o.RefType.Process, id=P.id)
        )
        result = client.calculate(setup)
        result.wait_until_ready()

        envi_flow = next(
            filter(lambda ei: ei.flow.id == e.id, result.get_envi_flows())
        )

        root = utree.of(result, envi_flow)
        self.assertAlmostEqual(12., root.result)
        self.assertAlmostEqual(2., root.direct_contribution)

        l1 = root.childs[0]
        self.assertAlmostEqual(10., l1.result)
        self.assertAlmostEqual(4., l1.direct_contribution)

        l2 = l1.childs[0]
        self.assertAlmostEqual(6., l2.result)
        self.assertAlmostEqual(1., l2.direct_contribution)

        l3 = l2.childs[0]
        self.assertAlmostEqual(5., l3.result)
        self.assertAlmostEqual(2., l3.direct_contribution)

        l4 = l3.childs[0]
        self.assertAlmostEqual(3., l4.result)
        self.assertAlmostEqual(0.5, l4.direct_contribution)

        l5 = l4.childs[0]
        self.assertAlmostEqual(2.5, l5.result)
        self.assertAlmostEqual(1.0, l5.direct_contribution)

        result.dispose()
        client.delete_all(Q, P, q, p, e, mass, units)


if __name__ == "__main__":
    unittest.main()
