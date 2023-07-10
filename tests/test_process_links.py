import unittest

import olca_schema as o

from config import client


class ProcessLinkTest(unittest.TestCase):
    def setUp(self):
        units = o.new_unit_group("Units of mass", "kg")
        mass = o.new_flow_property("Mass", units)
        e = o.new_elementary_flow("e", mass)
        p = o.new_product("p", mass)
        q = o.new_product("q", mass)

        P = o.new_process("P")
        o.new_output(P, p, amount=1).is_quantitative_reference = True
        o.new_output(P, e, amount=2)

        Q = o.new_process("Q")
        qref = o.new_output(Q, q, amount=1)
        qref.is_quantitative_reference = True
        linked_exchange = o.new_input(Q, p, 21)

        client.put_all(units, mass, e, p, q, P, Q)
        self.entities = [units, mass, e, p, q, P, Q]

        system = o.ProductSystem(name="System Q")
        system.ref_process = Q.to_ref()
        system.ref_exchange = o.ExchangeRef(internal_id=qref.internal_id)
        system.target_amount = 1
        system.target_flow_property = qref.flow_property
        system.target_unit = qref.unit

        system.processes = [Q.to_ref(), P.to_ref()]
        system.process_links = [
            o.ProcessLink(
                provider=P.to_ref(),
                process=Q.to_ref(),
                exchange=o.ExchangeRef(internal_id=linked_exchange.internal_id),
                flow=p.to_ref(),
            )
        ]
        client.put(system)
        self.system = system

    def tearDown(self):
        client.delete_all(*self.entities)
        client.delete(self.system)

    def test_process_links(self):
        system = client.get(o.ProductSystem, self.system.id)
        self.assertIsNotNone(system.process_links)
        self.assertEqual(1, len(system.process_links))

    def test_calculation(self):
        setup = o.CalculationSetup(target=self.system.to_ref())
        result = client.calculate(setup)
        result.wait_until_ready()
        e = next(
            filter(
                lambda ei: ei.envi_flow.flow.name == "e",
                result.get_total_flows(),
            )
        )
        self.assertAlmostEqual(42.0, e.amount)
        result.dispose()


if __name__ == "__main__":
    unittest.main()
