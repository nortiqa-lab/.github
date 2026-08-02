import unittest

from nl.auth import is_authorized


class AuthTests(unittest.TestCase):
    def test_fail_closed_empty(self):
        self.assertFalse(is_authorized("1", "1", users=[], chats=[], fail_closed=True))

    def test_user_allow(self):
        self.assertTrue(is_authorized("42", "9", users=["42"], chats=[]))

    def test_chat_allow(self):
        self.assertTrue(is_authorized("1", "99", users=[], chats=["99"]))

    def test_deny(self):
        self.assertFalse(is_authorized("1", "2", users=["42"], chats=["99"]))


if __name__ == "__main__":
    unittest.main()
