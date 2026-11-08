import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab import database, safe_lookup, safe_role_lookup, vulnerable_lookup


class QueryTests(unittest.TestCase):
    def setUp(self):
        self.db = database()

    def tearDown(self):
        self.db.close()

    def test_normal_query(self):
        self.assertEqual(safe_lookup(self.db, "alice"), [("alice", "analyst")])

    def test_lab_payload_exposes_unsafe_condition(self):
        self.assertEqual(len(vulnerable_lookup(self.db, "' OR '1'='1")), 3)

    def test_bound_parameter_blocks_condition_change(self):
        self.assertEqual(safe_lookup(self.db, "' OR '1'='1"), [])

    def test_safe_role_filter(self):
        self.assertEqual(safe_role_lookup(self.db, "engineer"), [("bob",)])

    def test_role_filter_treats_payload_as_data(self):
        self.assertEqual(safe_role_lookup(self.db, "' OR '1'='1"), [])


if __name__ == "__main__":
    unittest.main()
