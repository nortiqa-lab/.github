import os
import unittest

from nl.service import process_message


class ServiceTests(unittest.TestCase):
    def setUp(self):
        os.environ["TELEGRAM_ALLOWED_USER_IDS"] = "42"
        os.environ.pop("TELEGRAM_ALLOWED_CHAT_IDS", None)
        os.environ["NL_HANDOFF_ENABLED"] = "0"

    def test_unauthorized(self):
        r = process_message("/help", user_id="7", live_health=False)
        self.assertFalse(r.authorized)
        self.assertIn("No autorizado", r.reply)

    def test_help(self):
        r = process_message("/help", user_id="42", live_health=False)
        self.assertTrue(r.ok)
        self.assertIn("ROLE: bridge", r.reply)

    def test_promote_blocked(self):
        r = process_message("/ops promote staging to prod", user_id="42", live_health=False)
        self.assertEqual(r.zone, "red")
        self.assertIn("BLOCKED:", r.reply)

    def test_orch_brief(self):
        r = process_message("/orch pending work", user_id="42", live_health=False)
        self.assertEqual(r.role, "NL-ORCH")
        self.assertIn("ROLE: NL-ORCH", r.reply)


if __name__ == "__main__":
    unittest.main()
