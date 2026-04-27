import unittest

import olca_schema as o
from config import client


class GetTest(unittest.TestCase):
    def setUp(self):
        self.units = o.new_unit_group("Units of mass", "kg")
        self.mass = o.new_flow_property("Mass", self.units)
        client.put_all(self.units, self.mass)

    def tearDown(self):
        client.delete_all(self.mass, self.units)

    def test_get_for_name(self):
        mass = client.get(o.FlowProperty, name="Mass")
        assert mass is not None
        self.assertEqual("Mass", mass.name)

    def test_get_for_id(self):
        mass = client.get(o.FlowProperty, name="Mass")
        assert mass and mass.unit_group
        group = client.get(o.UnitGroup, mass.unit_group.id)
        assert group and group.units
        self.assertEqual(
            "kg", next(filter(lambda u: u.is_ref_unit, group.units)).name
        )

    def test_get_all(self):
        props = client.get_all(o.FlowProperty)
        mass = next(filter(lambda p: p.name == "Mass", props))
        self.assertIsNotNone(mass)

    def test_get_perc(self):
        name = "yoghurt, 12% fat"
        flow = o.new_product(name, self.mass)
        client.put(flow)
        saved = client.get(o.Flow, name=name)
        assert saved
        self.assertEqual(name, saved.name)
        client.delete(saved)


if __name__ == "__main__":
    unittest.main()
