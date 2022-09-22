import unittest

import olca as ipc
import olca_schema as lca


class CrudTest(unittest.TestCase):

    def test_unit_group(self):
        client = ipc.Client()

        # create a unit group
        units = lca.new_unit_group('Units of mass', 'kg')
        client.insert(units)
        units = client.get(lca.UnitGroup, units.id)
        self.assertEqual('kg', units.units[0].name)

        # create a flow property
        mass = lca.new_flow_property('Mass', units)
        client.insert(mass)
        mass = client.get(lca.FlowProperty, mass.id)
        self.assertEqual(units.id, mass.unit_group.id)

        # update the unit group
        units.default_flow_property = mass.to_ref()
        client.update(units)
        units = client.get(lca.UnitGroup, units.id)
        self.assertEqual(mass.id, units.default_flow_property.id)

        # delete everything
        client.delete(mass)
        client.delete(units)
        self.assertIsNone(client.get(lca.UnitGroup, units.id))
        self.assertIsNone(client.get(lca.FlowProperty, mass.id))

        client.close()
