import unittest

import olca_ipc as ipc
import olca_schema as schema
import olca_schema.results as results


class SimpleCalculatioTest(unittest.TestCase):
    def setUp(self):
        units = schema.new_unit_group("Units of mass", "kg")
        mass = schema.new_flow_property("Mass", units)
        e = schema.new_elementary_flow("e", mass)
        p = schema.new_product("p", mass)
        process = schema.new_process("P")
        schema.new_output(process, p, amount=1).is_quantitative_reference = True
        schema.new_output(process, e, amount=21)

        self.client = ipc.Client()
        self.process = process
        self.e = e
        self.entities = [units, mass, e, p, process]
        for entity in self.entities:
            self.client.put(entity)

        setup = results.CalculationSetup(
            target=schema.Ref(model_type="Process", id=process.id),
            amount=2,  # kg
        )
        self.result = self.client.calculate(setup)
        self.result.wait_until_ready()

    def tearDown(self):
        self.result.dispose()
        self.entities.reverse()
        for entity in self.entities:
            self.client.delete(entity)

    def test_tech_flow(self):
        tech_flow = self.get_tech_flow()
        self.assertEqual("P", tech_flow.provider.name)
        self.assertEqual("p", tech_flow.flow.name)
        self.assertEqual("kg", tech_flow.flow.ref_unit)

    def test_envi_flow(self):
        envi_flow = self.get_envi_flow()
        self.assertEqual("e", envi_flow.flow.name)
        self.assertEqual("kg", envi_flow.flow.ref_unit)

    def get_tech_flow(self) -> results.TechFlow:
        tech_flows = self.result.get_tech_flows()
        for tech_flow in tech_flows:
            if tech_flow.provider and tech_flow.provider.id == self.process.id:
                return tech_flow
        raise ValueError("tech. flow not found")

    def get_envi_flow(self) -> results.EnviFlow:
        envi_flows = self.result.get_envi_flows()
        for envi_flow in envi_flows:
            if envi_flow.flow and envi_flow.flow.id == self.e.id:
                return envi_flow
        raise ValueError("envi. flow not found")


if __name__ == "__main__":
    unittest.main()
