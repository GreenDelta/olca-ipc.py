import unittest
from functools import reduce

import olca_schema as o

from config import client


class AnalysisGroupsTest(unittest.TestCase):

    def test_analysis_groups(self):
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
        sys_ref = client.create_product_system(P)
        system = client.get(o.ProductSystem, sys_ref.id)

        system.analysis_groups = [
            o.AnalysisGroup(name="Top", processes=[P.to_ref()]),
            o.AnalysisGroup(name="Sub", processes=[Q.to_ref()]),
        ]
        client.put(system)

        setup = o.CalculationSetup(target=sys_ref)
        result = client.calculate(setup)
        result.wait_until_ready()
        e_groups: dict[str, float] = reduce(
            lambda d, v: d | {v.group: v.amount},
            result.get_grouped_flow_results_of(
                o.EnviFlow(e.to_ref(), is_input=False)
            ),
            {},
        )

        self.assertAlmostEqual(2.0, e_groups["Top"])
        self.assertAlmostEqual(10.0, e_groups["Sub"])
