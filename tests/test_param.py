import unittest

import olca_schema as o

from config import client


class ParamTest(unittest.TestCase):
    def test_global_params(self):
        x = o.new_parameter("X", 4.0)
        y = o.new_parameter("Y", "X * 10")
        client.put(x)
        client.put(y)

        x = client.get(o.Parameter, x.id)
        y = client.get(o.Parameter, y.id)
        self.assertEqual("X", x.name)
        self.assertEqual(o.ParameterScope.GLOBAL_SCOPE, x.parameter_scope)
        self.assertEqual(4, x.value)
        self.assertTrue(x.is_input_parameter)
        client.delete(x)

        self.assertEqual("Y", y.name)
        self.assertEqual("X * 10", y.formula)
        self.assertEqual(o.ParameterScope.GLOBAL_SCOPE, y.parameter_scope)
        self.assertFalse(y.is_input_parameter)
        client.delete(y)


if __name__ == "__main__":
    unittest.main()
