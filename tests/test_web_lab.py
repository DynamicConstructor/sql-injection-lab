import json
import sys
import threading
import unittest
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from web_lab import compare, make_server


class WebLabTests(unittest.TestCase):
    def test_normal_input_returns_same_row(self):
        result = compare("alice")
        self.assertEqual(result["unsafe"]["rows"], result["parameterized"]["rows"])

    def test_controlled_predicate_is_blocked_by_parameterization(self):
        result = compare("' OR '1'='1")
        self.assertEqual(len(result["unsafe"]["rows"]), 3)
        self.assertEqual(result["parameterized"]["rows"], [])

    def test_unexpected_quote_has_labeled_unsafe_error(self):
        self.assertEqual(compare("'")["unsafe"]["error"], "OperationalError")

    def test_length_limit(self):
        with self.assertRaises(ValueError):
            compare("a" * 201)

    def test_loopback_http_api(self):
        server = make_server(0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/api/compare?username={quote('alice')}"
            with urlopen(url, timeout=3) as response:
                data = json.load(response)
            self.assertEqual(data["parameterized"]["rows"], [["alice", "analyst"]])
            self.assertEqual(server.server_address[0], "127.0.0.1")
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
