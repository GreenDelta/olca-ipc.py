import unittest

import olca.schema as schema


class TestModel(unittest.TestCase):

    def test_enums(self):
        self.assertEqual(schema.FlowType.ELEMENTARY_FLOW.value,
                         'ELEMENTARY_FLOW')


if __name__ == '__main__':
    unittest.main()
