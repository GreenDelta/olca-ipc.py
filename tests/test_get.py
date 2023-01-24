import unittest

import olca_ipc as ipc
import olca_schema as schema


class GetTest(unittest.TestCase):
    """A test for getting entities from the server.

    Only works when a server is running with a database that contains the
    standard flow properties and units.
    """

    def test_get_for_name(self):
        client = ipc.Client()
        mass = client.get(schema.FlowProperty, name="Mass")
        self.assertEqual("Mass", mass.name)

    def test_get_for_id(self):
        client = ipc.Client()
        mass = client.get(schema.FlowProperty, name="Mass")
        group = client.get(schema.UnitGroup, mass.unit_group.id)
        self.assertEqual(
            "kg", next(filter(lambda u: u.is_ref_unit, group.units)).name
        )

    def test_get_all(self):
        client = ipc.Client()
        props = client.get_all(schema.FlowProperty)
        mass = next(filter(lambda p: p.name == "Mass", props))
        self.assertIsNotNone(mass)


if __name__ == "__main__":
    unittest.main()
