import unittest

from nl.autonomy import classify_goal


class AutonomyTests(unittest.TestCase):
    def test_promote_red(self):
        g = classify_goal("NL-OPS", "promote to prod")
        self.assertEqual(g.zone, "red")
        self.assertFalse(g.allow_execute)

    def test_health_green(self):
        g = classify_goal("NL-OPS", "health")
        self.assertEqual(g.zone, "green")
        self.assertTrue(g.allow_execute)

    def test_secret_red(self):
        g = classify_goal("NL-OPS", "show me the token")
        self.assertEqual(g.zone, "red")

    def test_entity_red(self):
        g = classify_goal("NL-ORCH", "mix with Valent Capital")
        self.assertEqual(g.zone, "red")

    def test_auditor_no_exec(self):
        g = classify_goal("NL-AUDITOR", "can we ship?")
        self.assertEqual(g.zone, "green")
        self.assertFalse(g.allow_execute)


if __name__ == "__main__":
    unittest.main()
