import unittest

import boto3

from data.dynamodb.UserData import UserData


class TestUserData(unittest.TestCase):
    def setUp(self):
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        self.toTest = UserData(dynamodb)

    def test_01_add_user(self):
        user = self.toTest.add_user("HEBELEK")
        self.assertIsNotNone(user)
        self.assertEqual(user.discord_user_id, "HEBELEK")

    def test_02_get_user(self):
        user = self.toTest.get_user("HEBELEK")
        self.assertIsNotNone(user)
        self.assertEqual(user.discord_user_id, "HEBELEK")
        self.assertEqual(user.is_admin, 0)

    def test_03_get_or_create_user(self):
        user = self.toTest.get_or_create_user("TODELETE")
        self.assertIsNotNone(user)
        self.assertEqual(user.discord_user_id, "TODELETE")
        self.assertEqual(user.is_admin, 0)

    def test_04_get_or_create_user(self):
        self.toTest.delete_user("TODELETE")
        deleted_user = self.toTest.get_user("TODELETE")
        self.assertIsNone(deleted_user)


# driver code
if __name__ == '__main__':
    unittest.main()
