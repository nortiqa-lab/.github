import unittest

from nl.contracts import format_reply


class ContractTests(unittest.TestCase):
    def test_format_contains_fields(self):
        text = format_reply("NL-OPS", done="ok", verify="200", next_step="wait")
        for key in ("ROLE:", "CANON:", "DONE:", "VERIFY:", "BLOCKED:", "NEXT:"):
            self.assertIn(key, text)

    def test_truncate(self):
        text = format_reply("NL-ORCH", extra="x" * 5000, max_chars=200)
        self.assertLessEqual(len(text), 200)
        self.assertIn("truncated", text)


if __name__ == "__main__":
    unittest.main()
