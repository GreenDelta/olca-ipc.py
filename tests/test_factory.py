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

    def test_flow_property(self):
        units = olca.unit_group_of('Units of mass', 'kg')
        mass = olca.flow_property_of('Mass', units)
        self.assertEqual(mass.olca_type, 'FlowProperty')
        self.assertEqual(mass.name, 'Mass')
        self.assertEqual(mass.unit_group.name, units.name)

    def test_flow(self):
        units = olca.unit_group_of('Units of mass', 'kg')
        mass = olca.flow_property_of('Mass', units)
        steel = olca.flow_of('Steel', olca.FlowType.PRODUCT_FLOW, mass)
        self.assertEqual(steel.olca_type, 'Flow')
        self.assertEqual(steel.name, 'Steel')
        self.assertEqual(steel.flow_properties[0].flow_property.name, 'Mass')

    def test_product_flow(self):
        units = olca.unit_group_of('Units of mass', 'kg')
        mass = olca.flow_property_of('Mass', units)
        steel = olca.product_flow_of('Steel', mass)
        self.assertEqual(olca.FlowType.PRODUCT_FLOW, steel.flow_type)
        self.assertEqual(steel.olca_type, 'Flow')
        self.assertEqual(steel.name, 'Steel')
        self.assertEqual(steel.flow_properties[0].flow_property.name, 'Mass')

    def test_waste_flow(self):
        units = olca.unit_group_of('Units of mass', 'kg')
        mass = olca.flow_property_of('Mass', units)
        scrap = olca.waste_flow_of('Scrap', mass)
        self.assertEqual(olca.FlowType.WASTE_FLOW, scrap.flow_type)
        self.assertEqual(scrap.olca_type, 'Flow')
        self.assertEqual(scrap.name, 'Scrap')
        self.assertEqual(scrap.flow_properties[0].flow_property.name, 'Mass')

    def test_elementary_flow(self):
        units = olca.unit_group_of('Units of mass', 'kg')
        mass = olca.flow_property_of('Mass', units)
        co2 = olca.elementary_flow_of('CO2', mass)
        self.assertEqual(olca.FlowType.ELEMENTARY_FLOW, co2.flow_type)
        self.assertEqual(co2.olca_type, 'Flow')
        self.assertEqual(co2.name, 'CO2')
        self.assertEqual(co2.flow_properties[0].flow_property.name, 'Mass')

    def test_process(self):
        process = olca.process_of('Steel production')
        self.assertEqual(process.olca_type, 'Process')
        self.assertEqual(process.name, 'Steel production')

    def test_exchange(self):
        units = olca.unit_group_of('Units of mass', 'kg')
        mass = olca.flow_property_of('Mass', units)
        steel = olca.product_flow_of('Steel', mass)
        process = olca.process_of('Steel production')
        output = olca.exchange_of(process, steel)
        output.quantitative_reference = True
        self.assertEqual(1, len(process.exchanges))
        self.assertEqual(output.olca_type, 'Exchange')
        self.assertEqual(output.flow.name, 'Steel')
        self.assertEqual(output.amount, 1.0)


if __name__ == '__main__':
    unittest.main()
