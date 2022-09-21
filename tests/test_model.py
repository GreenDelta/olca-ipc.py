import unittest

import olca_schema as schema


class TestModel(unittest.TestCase):

    def test_enums(self):
        self.assertEqual(
            schema.FlowType.ELEMENTARY_FLOW.value, 'ELEMENTARY_FLOW')
        self.assertEqual(
            schema.FlowType.ELEMENTARY_FLOW, schema.FlowType('ELEMENTARY_FLOW'))

    def test_json_conversion(self):
        p1 = schema.Process(
            name='a process',
            process_type=schema.ProcessType.UNIT_PROCESS)
        p2 = schema.Process.from_json(p1.to_json())
        self.assertEqual('a process', p2.name)
        self.assertEqual(schema.ProcessType.UNIT_PROCESS, p2.process_type)

    def test_type_tag(self):
        flow = schema.Flow()
        self.assertEqual('Flow', flow.to_ref().model_type)
        flow_dict = flow.to_dict()
        self.assertEqual('Flow', flow_dict['@type'])


if __name__ == '__main__':
    unittest.main()
