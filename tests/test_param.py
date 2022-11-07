import olca as ipc
import olca_schema as lca

import unittest


class ParamTest(unittest.TestCase):

    def test_global_params(self):
        x = lca.new_parameter('X', 4.0)
        y = lca.new_parameter('Y', 'X * 10')
        client = ipc.Client()
        client.insert(x)
        client.insert(y)

        x = client.get(lca.Parameter, x.id)
        y = client.get(lca.Parameter, y.id)
        self.assertEqual('X', x.name)
        self.assertEqual(lca.ParameterScope.GLOBAL_SCOPE, x.parameter_scope)
        self.assertEqual(4, x.value)
        self.assertTrue(x.is_input_parameter)

        self.assertEqual('Y', y.name)
        self.assertEqual('X * 10', y.formula)
        self.assertEqual(lca.ParameterScope.GLOBAL_SCOPE, y.parameter_scope)
        self.assertFalse(y.is_input_parameter)
        # client.delete(param)
