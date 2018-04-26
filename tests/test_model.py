import unittest

import olca.schema as schema


class TestModel(unittest.TestCase):

    def test_enums(self):
        self.assertEqual(schema.FlowType.ELEMENTARY_FLOW.value,
                         'ELEMENTARY_FLOW')
        self.assertEqual(schema.FlowType.ELEMENTARY_FLOW,
                         schema.FlowType('ELEMENTARY_FLOW'))

    def test_json_conversion(self):
        p = schema.Process()
        p.name = 'a process'
        jdict = p.to_json()
        self.assertEqual('a process', jdict['name'])

if __name__ == '__main__':
    unittest.main()
