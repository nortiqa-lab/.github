import unittest

from nl.router import route_message


class RouterTests(unittest.TestCase):
    def test_help(self):
        r = route_message("/help")
        self.assertEqual(r.kind, "bridge")
        self.assertEqual(r.action, "help")

    def test_ops_command(self):
        r = route_message("/ops health")
        self.assertEqual(r.role, "NL-OPS")
        self.assertEqual(r.goal, "health")

    def test_bot_mention(self):
        r = route_message("/ops@NortiqaServidorOpsBot health")
        self.assertEqual(r.role, "NL-OPS")
        self.assertEqual(r.goal, "health")

    def test_role_prefix(self):
        r = route_message("NL-BUILDER: fix readme")
        self.assertEqual(r.role, "NL-BUILDER")
        self.assertEqual(r.goal, "fix readme")

    def test_free_text_default_orch(self):
        r = route_message("qué queda pendiente?")
        self.assertEqual(r.role, "NL-ORCH")

    def test_ops_keyword(self):
        r = route_message("corre healthcheck staging")
        self.assertEqual(r.role, "NL-OPS")


if __name__ == "__main__":
    unittest.main()
