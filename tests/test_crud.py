import unittest

import olca_schema as o

from config import client


class CrudTest(unittest.TestCase):
    def test_unit_group(self):

        # create a unit group
        units = o.new_unit_group("Units of mass", "kg")
        client.put(units)
        units = client.get(o.UnitGroup, units.id)
        self.assertEqual("kg", units.units[0].name)

        # create a flow property
        mass = o.new_flow_property("Mass", units)
        client.put(mass)
        mass = client.get(o.FlowProperty, mass.id)
        self.assertEqual(units.id, mass.unit_group.id)

        # update the unit group
        units.default_flow_property = mass.to_ref()
        client.put(units)
        units = client.get(o.UnitGroup, units.id)
        self.assertEqual(mass.id, units.default_flow_property.id)

        # delete everything
        client.delete(mass)
        client.delete(units)
        self.assertIsNone(client.get(o.UnitGroup, units.id))
        self.assertIsNone(client.get(o.FlowProperty, mass.id))

    def test_process(self):
        units = o.new_unit_group("Mass units", "kg")
        mass = o.new_flow_property("Mass", units)
        steel = o.new_product("Steel", mass)
        process = o.new_process("Steel production")
        o.new_output(process, steel).is_quantitative_reference = True

        for e in [units, mass, steel, process]:
            client.put(e)
        assert process.id is not None
        process = client.get(o.Process, process.id)

        output = process.exchanges[0]
        self.assertEqual(steel.id, output.flow.id)
        self.assertTrue(output.is_quantitative_reference)
        self.assertFalse(output.is_input)
        self.assertFalse(output.is_avoided_product)
        self.assertEqual(1.0, output.amount)

        for e in [process, steel, mass, units]:
            client.delete(e)


if __name__ == "__main__":
    unittest.main()
