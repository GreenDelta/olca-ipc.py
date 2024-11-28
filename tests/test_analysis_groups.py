import unittest
from functools import reduce

import olca_schema as o

from config import client


class AnalysisGroupsTest(unittest.TestCase):

    def test_analysis_groups(self):

        # create units & flows
        euro = o.Currency(id="euro", name="Euro", code="EUR")
        euro.ref_currency = euro.to_ref()
        units = o.new_unit_group("Units of mass", "kg")
        mass = o.new_flow_property("Mass", units)
        e = o.new_elementary_flow("e", mass)
        p = o.new_product("p", mass)
        q = o.new_product("q", mass)

        # create processes
        P = o.new_process("P")
        Q = o.new_process("Q")

        o.new_output(P, p, amount=1).is_quantitative_reference = True
        q_in = o.new_input(P, q, amount=1)
        q_in.default_provider = Q.to_ref()
        q_in.cost_value = 2
        q_in.currency = euro.to_ref()
        o.new_output(P, e, amount=2)

        o.new_output(Q, q, amount=1).is_quantitative_reference = True
        p_in = o.new_input(Q, p, amount=0.5)
        p_in.default_provider = P.to_ref()
        p_in.cost_value = 2
        p_in.currency = euro.to_ref()
        o.new_output(Q, e, amount=4)

        # create the LCIA method
        I = o.new_impact_category("I")
        o.new_impact_factor(I, e, 2.0)
        M = o.new_impact_method("M", I)

        # insert data & create the product system
        client.put_all(euro, units, mass, e, p, q, P, Q, I, M)
        sys_ref = client.create_product_system(P)
        system = client.get(o.ProductSystem, sys_ref.id)

        system.analysis_groups = [
            o.AnalysisGroup(name="Top", processes=[P.to_ref()]),
            o.AnalysisGroup(name="Sub", processes=[Q.to_ref()]),
        ]
        client.put(system)

        # calculate results
        setup = o.CalculationSetup(
            target=sys_ref, impact_method=M.to_ref(), with_costs=True
        )
        result = client.calculate(setup)
        result.wait_until_ready()

        # get & check the analysis group results of an intervention flow
        e_groups: dict[str, float] = reduce(
            lambda d, v: d | {v.group: v.amount},
            result.get_grouped_flow_results_of(
                o.EnviFlow(e.to_ref(), is_input=False)
            ),
            {},
        )
        self.assertAlmostEqual(2.0, e_groups["Top"])
        self.assertAlmostEqual(10.0, e_groups["Sub"])

        # get & check the analysis group results of an impact category
        i_groups: dict[str, float] = reduce(
            lambda d, v: d | {v.group: v.amount},
            result.get_grouped_impact_results_of(I.to_ref()),
            {},
        )
        self.assertAlmostEqual(4.0, i_groups["Top"])
        self.assertAlmostEqual(20.0, i_groups["Sub"])

        # get & check the analysis group results for costs
        c_groups: dict[str, float] = reduce(
            lambda d, v: d | {v.group: v.amount},
            result.get_grouped_cost_results(),
            {},
        )
        self.assertAlmostEqual(2.0, c_groups["Top"])
        self.assertAlmostEqual(6.0, c_groups["Sub"])

        # clean up
        result.dispose()
        client.delete_all(system, M, I, P, Q, p, q, e, mass, units, euro)
