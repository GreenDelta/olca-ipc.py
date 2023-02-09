import unittest

import olca_schema as o

from config import client


@unittest.SkipTest
class GetTest(unittest.TestCase):
    """A test for getting entities from the server.

    Only works when a server is running with a database that contains the
    standard flow properties and units.
    """

    def test_get_for_name(self):
        mass = client.get(o.FlowProperty, name="Mass")
        self.assertEqual("Mass", mass.name)

    def test_get_for_id(self):
        mass = client.get(o.FlowProperty, name="Mass")
        group = client.get(o.UnitGroup, mass.unit_group.id)
        self.assertEqual(
            "kg", next(filter(lambda u: u.is_ref_unit, group.units)).name
        )

    def test_get_all(self):
        props = client.get_all(o.FlowProperty)
        mass = next(filter(lambda p: p.name == "Mass", props))
        self.assertIsNotNone(mass)


if __name__ == "__main__":
    unittest.main()
