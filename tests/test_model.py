import unittest

import olca


class TestModel(unittest.TestCase):

    def test_enums(self):
        self.assertEqual(olca.FlowType.ELEMENTARY_FLOW.value,
                         'ELEMENTARY_FLOW')
        self.assertEqual(olca.FlowType.ELEMENTARY_FLOW,
                         olca.FlowType('ELEMENTARY_FLOW'))

    def test_json_conversion(self):
        p1 = olca.Process()
        p1.name = 'a process'
        p1.process_type = olca.ProcessType.UNIT_PROCESS
        jdict = p1.to_json()
        p2 = olca.Process()
        p2.from_json(jdict)
        self.assertEqual('a process', p2.name)
        self.assertEqual(olca.ProcessType.UNIT_PROCESS, p2.process_type)


if __name__ == '__main__':
    unittest.main()
