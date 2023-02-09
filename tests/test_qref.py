import unittest

import olca_schema as o

from config import client


class TestQRef(unittest.TestCase):
    def test_qref(self):
        mass = client.get(o.FlowProperty, name="Mass")
        steel = o.new_product("Steel", mass)
        process = o.new_process("Steel production")
        o.new_exchange(process, steel).is_quantitative_reference = True
        client.put_all(steel, process)

        process = client.get(o.Process, process.id)
        qref = next(e for e in process.exchanges if e.is_quantitative_reference)
        self.assertEqual(steel.id, qref.flow.id)
        self.assertEqual(1, qref.amount)

        client.delete_all(process, steel)


if __name__ == "__main__":
    unittest.main()
