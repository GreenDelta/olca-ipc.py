import unittest
from unittest import mock

import olca_schema as o

from olca_ipc.rest import RestClient

_URL = "http://localhost:8080/"


class RestPathTest(unittest.TestCase):
    """Checks the request paths of the REST client; needs no server."""

    def setUp(self):
        self.client = RestClient(_URL)

    def test_delete(self):
        cases = [
            (o.DQSystem(id="dq"), "dq-systems/dq"),
            (o.Ref(ref_type=o.RefType.DQSystem, id="dq"), "dq-systems/dq"),
            (o.FlowProperty(id="fp"), "flow-properties/fp"),
            (o.ProductSystem(id="ps"), "product-systems/ps"),
        ]
        for entity, path in cases:
            with self.subTest(path=path):
                with mock.patch("requests.delete") as req:
                    req.return_value.status_code = 200
                    req.return_value.json.return_value = {"@id": entity.id}
                    self.client.delete(entity)
                self.assertEqual(f"{_URL}data/{path}", req.call_args.args[0])

    def test_delete_without_path(self):
        # a Ref without a type has no REST path, so no request is sent
        with mock.patch("requests.delete") as req:
            self.assertIsNone(self.client.delete(o.Ref(id="x")))
        req.assert_not_called()


if __name__ == "__main__":
    unittest.main()
