import unittest

import olca


class TestFactory(unittest.TestCase):

    def test_unit(self):
        kg = olca.unit_of('kg')
        self.assertEqual(kg.olca_type, 'Unit')
        self.assertEqual(kg.name, 'kg')
        self.assertEqual(kg.conversion_factor, 1.0)

    def test_unit_group(self):
        units = olca.unit_group_of('Units of mass', 'kg')
        self.assertEqual(units.olca_type, 'UnitGroup')
        self.assertEqual(units.units[0].name, 'kg')


if __name__ == '__main__':
    unittest.main()
