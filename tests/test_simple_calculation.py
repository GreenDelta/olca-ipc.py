import unittest

import olca_schema as o

from config import client


class SimpleCalculationTest(unittest.TestCase):
    def setUp(self):
        units = o.new_unit_group("Units of mass", "kg")
        mass = o.new_flow_property("Mass", units)
        e = o.new_elementary_flow("e", mass)
        p = o.new_product("p", mass)
        process = o.new_process("P")
        o.new_output(process, p, amount=1).is_quantitative_reference = True
        o.new_output(process, e, amount=21)

        i = o.new_impact_category("i")
        o.new_impact_factor(i, e, 0.5)
        method = o.new_impact_method("M", i)

        self.process = process
        self.e = e
        self.entities = [units, mass, e, p, process, i, method]
        for entity in self.entities:
            client.put(entity)

        setup = o.CalculationSetup(
            target=process.to_ref(),
            impact_method=method.to_ref(),
            amount=2,  # kg
        )
        self.result = client.calculate(setup)
        self.result.wait_until_ready()

    def tearDown(self):
        self.result.dispose()
        self.entities.reverse()
        for entity in self.entities:
            client.delete(entity)

    def test_demand(self):
        demand = self.result.get_demand()
        self.assertEqual("P", demand.tech_flow.provider.name)
        self.assertEqual("p", demand.tech_flow.flow.name)
        self.assertEqual(2, demand.amount)

    def test_tech_flow(self):
        tech_flow = self.get_tech_flow()
        self.assertEqual("P", tech_flow.provider.name)
        self.assertEqual("p", tech_flow.flow.name)
        self.assertEqual("kg", tech_flow.flow.ref_unit)

    def test_envi_flow(self):
        envi_flow = self.get_envi_flow()
        self.assertEqual("e", envi_flow.flow.name)
        self.assertEqual("kg", envi_flow.flow.ref_unit)

    def test_impact(self):
        impact = self.get_impact()
        self.assertEqual("i", impact.name)

    def test_tech_flow_values(self):
        r = self.result
        seq = [
            # todo: scaling factors etc.
            (r.get_total_requirements(), 2)
        ]
        for (values, expected) in seq:
            value: o.TechFlowValue = next(
                filter(
                    lambda x: x.tech_flow.provider.id == self.process.id, values
                )
            )
            self.assertEqual(expected, value.amount)

    def test_envi_flow_values(self):
        tech_flow = self.get_tech_flow()
        xs = [
            self.result.get_total_flows(),
            self.result.get_direct_interventions_of(tech_flow),
            self.result.get_total_interventions_of(tech_flow),
        ]
        for r in xs:
            value: o.EnviFlowValue = next(
                filter(lambda x: x.envi_flow.flow.id == self.e.id, r)
            )
            self.assertEqual(42, value.amount)

    def test_envi_flow_value(self):
        envi_flow = self.get_envi_flow()
        tech_flow = self.get_tech_flow()
        values = [
            self.result.get_total_flow_value_of(envi_flow),
            self.result.get_total_intervention_of(envi_flow, tech_flow),
            self.result.get_direct_intervention_of(envi_flow, tech_flow),
        ]
        for v in values:
            self.assertEqual(42, v.amount)
            self.assertEqual("e", v.envi_flow.flow.name)
            self.assertEqual("kg", v.envi_flow.flow.ref_unit)

    def test_impact_values(self):
        tech_flow = self.get_tech_flow()
        xs = [
            self.result.get_total_impacts(),
            self.result.get_direct_impacts_of(tech_flow),
            self.result.get_total_impacts_of(tech_flow),
        ]
        for r in xs:
            value: o.ImpactValue = r[0]
            self.assertEqual(21, value.amount)

    def test_impact_value(self):
        tech_flow = self.get_tech_flow()
        impact = self.get_impact()
        values = [
            self.result.get_total_impact_value_of(impact),
            self.result.get_direct_impact_of(impact, tech_flow),
            self.result.get_total_impact_of(impact, tech_flow),
        ]
        for v in values:
            self.assertEqual(21, v.amount)
            self.assertEqual("i", v.impact_category.name)

    def get_tech_flow(self) -> o.TechFlow:
        tech_flows = self.result.get_tech_flows()
        for tech_flow in tech_flows:
            if tech_flow.provider and tech_flow.provider.id == self.process.id:
                return tech_flow
        raise ValueError("tech. flow not found")

    def get_envi_flow(self) -> o.EnviFlow:
        envi_flows = self.result.get_envi_flows()
        for envi_flow in envi_flows:
            if envi_flow.flow and envi_flow.flow.id == self.e.id:
                return envi_flow
        raise ValueError("envi. flow not found")

    def get_impact(self) -> o.Ref:
        impacts = self.result.get_impact_categories()
        for i in impacts:
            if i.name == "i":
                return i
        raise ValueError("impact category not found")


if __name__ == "__main__":
    unittest.main()
