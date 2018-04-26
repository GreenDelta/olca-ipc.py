import unittest

import olca.schema as schema


class TestModel(unittest.TestCase):

    def test_enums(self):
        self.assertEqual(schema.FlowType.ELEMENTARY_FLOW.value,
                         'ELEMENTARY_FLOW')
        self.assertEqual(schema.FlowType.ELEMENTARY_FLOW,
                         schema.FlowType('ELEMENTARY_FLOW'))

    def test_json_conversion(self):
        p1 = schema.Process()
        p1.name = 'a process'
        p1.process_type = schema.ProcessType.UNIT_PROCESS
        jdict = p1.to_json()
        p2 = schema.Process()
        p2.from_json(jdict)
        self.assertEqual('a process', p2.name)
        self.assertEqual(schema.ProcessType.UNIT_PROCESS, p2.process_type)

if __name__ == '__main__':
    unittest.main()
