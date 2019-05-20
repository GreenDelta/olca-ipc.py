import unittest

import olca.units as units


class TestUnits(unittest.TestCase):

    def test_unit_ref(self):
        ref = units.unit_ref('m2')
        self.assertEqual(
            '3ce61faa-5716-41c1-aef6-b5920054acc9',
            ref.id),
        self.assertEqual('m2', ref.name)

    def test_group_ref(self):
        ref = units.group_ref('m2')
        self.assertEqual(
            '93a60a57-a3c8-18da-a746-0800200c9a66',
            ref.id),
        self.assertEqual('Units of area', ref.name)

    def test_prop_ref(self):
        ref = units.property_ref('m2')
        self.assertEqual(
            '93a60a56-a3c8-19da-a746-0800200c9a66',
            ref.id),
        self.assertEqual('Area', ref.name)


if __name__ == '__main__':
    unittest.main()
