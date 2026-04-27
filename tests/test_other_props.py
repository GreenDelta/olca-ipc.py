import unittest

import olca_schema as o
from config import client


class OtherPropertiesTest(unittest.TestCase):
    def test_additional_properties(self):
        units = o.new_unit_group("Units of mass", "kg")
        mass = o.new_flow_property("Mass", units)

        flow = o.new_product("Product", mass)
        flow.other_properties = {
            "some": "more",
            "properties": ["that", "you", "can"],
            "add": {
                "asYouLike": [
                    1,
                    2,
                ]
            },
        }

        client.put_all(units, mass, flow)
        saved_flow = client.get(o.Flow, flow.id)
        assert saved_flow is not None

        props = saved_flow.other_properties
        assert props is not None
        self.assertEqual([1, 2], props["add"]["asYouLike"])

        client.delete_all(flow, mass, units)
