import unittest
import gspread

from data.sheets.UserData import UserData


class TestUserData(unittest.TestCase):
    def setUp(self):
        gc = gspread.service_account(filename='../../../sheet-auth.json')
        usr_sheet = gc.open("Settings")
        self.toTest = UserData(usr_sheet)

    def test_add_user(self):
        user = self.toTest.add_user("HEBELEK")
        self.assertIsNotNone(user)
        self.assertGreater(user.id, 0)

    def test_add_user_row(self):
        user = self.toTest.add_user_row("GUBELEK", '', 1)
        self.assertIsNotNone(user)
        self.assertGreater(user.id, 0)
        self.assertEqual(user.discord_user_id, "GUBELEK")
        self.assertEqual(user.is_admin, 1)

    def test_get_user(self):
        user = self.toTest.get_user("GUBELEK")
        self.assertIsNotNone(user)
        self.assertGreater(user.id, 0)
        self.assertEqual(user.discord_user_id, "GUBELEK")
        self.assertEqual(user.is_admin, 1)


# driver code
if __name__ == '__main__':
    unittest.main()
