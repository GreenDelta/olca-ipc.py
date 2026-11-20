import unittest
from unittest import mock
from urllib.parse import unquote, urlsplit

import olca_schema as o
import requests

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

    def test_get_usage(self):
        with mock.patch("requests.get") as req:
            req.return_value.status_code = 200
            req.return_value.json.return_value = [
                {"@type": "Process", "@id": "p", "name": "P"}
            ]
            refs = self.client.get_usage(o.Flow, "f")
        self.assertEqual(f"{_URL}data/flows/f/usage", req.call_args.args[0])
        self.assertEqual(1, len(refs))
        self.assertEqual("p", refs[0].id)

    def test_delete_without_path(self):
        # a Ref without a type has no REST path, so no request is sent
        with mock.patch("requests.delete") as req:
            self.assertIsNone(self.client.delete(o.Ref(id="x")))
        req.assert_not_called()

    def test_get_for_name(self):
        # the server must receive the full name; checks the URL as requests
        # sends it, where `#` starts a fragment and `?` a query
        names = [
            "Mass",
            "yoghurt, 12% fat",
            "Gas, natural/m3",
            "#2 fuel oil",
            "steel? or iron",
            "blend 50%41",
            "Ölsaaten (rapeseed)",
        ]
        prefix = "/data/flows/name/"
        for name in names:
            with self.subTest(name=name):
                with mock.patch("requests.get") as req:
                    req.return_value.status_code = 200
                    req.return_value.json.return_value = {"@id": "f"}
                    self.client.get(o.Flow, name=name)
                sent = requests.Request("GET", req.call_args.args[0])
                url = urlsplit(sent.prepare().url)
                self.assertEqual("", url.query)
                self.assertEqual("", url.fragment)
                self.assertTrue(url.path.startswith(prefix))
                self.assertEqual(name, unquote(url.path[len(prefix) :]))

    def test_get_descriptor_for_name(self):
        # there is no REST route for a descriptor by name, so the client
        # searches the descriptors of the type
        refs = [
            {"@type": "Flow", "@id": "f1", "name": "steel"},
            {"@type": "Flow", "@id": "f2", "name": "iron"},
        ]
        for name, uid in [("iron", "f2"), ("copper", None)]:
            with self.subTest(name=name):
                with mock.patch("requests.get") as req:
                    req.return_value.status_code = 200
                    req.return_value.json.return_value = refs
                    ref = self.client.get_descriptor(o.Flow, name=name)
                req.assert_called_once_with(f"{_URL}data/flows")
                self.assertEqual(uid, ref.id if ref else None)


if __name__ == "__main__":
    unittest.main()
