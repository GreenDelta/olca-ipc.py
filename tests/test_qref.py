import unittest

import olca_ipc as ipc
import olca_schema as lca


class TestQRef(unittest.TestCase):
    def test_qref(self):
        client = ipc.Client()
        mass = client.get(lca.FlowProperty, name="Mass")
        steel = lca.new_product("Steel", mass)
        client.put(steel)
        process = lca.new_process("Steel production")
        lca.new_exchange(process, steel).is_quantitative_reference = True
        client.put(process)

        process = client.get(lca.Process, process.id)
        qref = next(e for e in process.exchanges if e.is_quantitative_reference)
        self.assertEqual(steel.id, qref.flow.id)
        self.assertEqual(1, qref.amount)

        client.delete(process)
        client.delete(steel)


if __name__ == "__main__":
    unittest.main()
