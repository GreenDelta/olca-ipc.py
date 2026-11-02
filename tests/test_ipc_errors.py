import unittest
from unittest import mock

import olca_schema as o

from olca_ipc.ipc import Client, Result


class IpcErrorTest(unittest.TestCase):
    """Checks how the JSON-RPC client handles server errors; needs no server."""

    def setUp(self):
        self.client = Client()
        self.rpc_call = self.enterContext(mock.patch.object(Client, "rpc_call"))

    def test_get_all_on_error(self):
        self.rpc_call.return_value = (None, "-32000: failed")
        self.assertEqual([], self.client.get_all(o.Flow))

    def test_get_parameters_on_error(self):
        self.rpc_call.return_value = (None, "-32000: failed")
        with self.assertLogs(level="ERROR") as logs:
            params = self.client.get_parameters(o.Process, "p1")
        self.assertEqual([], params)
        self.assertIn("id=p1: -32000: failed", logs.output[0])

    def test_simulate_next_error_is_kept(self):
        result = Result(uid="r1", client=self.client, error=None)
        self.rpc_call.return_value = (None, "-32000: failed")
        state = result.simulate_next()
        self.assertEqual("-32000: failed", state.error)

        # the error is kept, like in the RestResult
        self.rpc_call.reset_mock()
        self.assertIs(state, result.get_state())
        self.assertIs(state, result.simulate_next())
        self.rpc_call.assert_not_called()

        # the result still exists on the server and must be disposed
        result.dispose()
        self.rpc_call.assert_called_once_with("result/dispose", {"@id": "r1"})

    def test_no_dispose_without_result(self):
        result = Result(uid="", client=self.client, error=o.ResultState())
        result.dispose()
        self.rpc_call.assert_not_called()


if __name__ == "__main__":
    unittest.main()
