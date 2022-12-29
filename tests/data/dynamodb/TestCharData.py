import unittest

import boto3

from data.dynamodb.CharacterData import CharacterData
from data.dynamodb.Models.InventoryItem import InventoryItem


class TestCharData(unittest.TestCase):

    def setUp(self):
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        self.toTest = CharacterData(dynamodb)

    # define a function
    def test_01_add_character(self):
        char = self.toTest.add_character("Test User", "me")
        self.assertEqual("Test User", char.name)
        self.assertEqual("me", char.owner)

    def test_02_get_all(self):
        char_list = self.toTest.get_all()
        self.assertEqual("Test User", char_list[0].name)
        self.assertEqual("me", char_list[0].owner)

    def test_02_get_character(self):
        char = self.toTest.get_character("Test User")
        self.assertEqual("Test User", char.name)

    def test_03_save_character(self):
        char = self.toTest.get_character("Test User")
        char.coins = 333
        self.toTest.save_data_obj(char)
        char = self.toTest.get_character("Test User")
        self.assertEqual(333, char.coins)

    def test_04_add_new_item_to_char(self):
        char = self.toTest.get_character("Test User")
        char.add_item("Item A", 1)
        char.add_item("Item B", 1)
        self.toTest.save_data_obj(char)

    def test_05_remove_existing_item_from_char(self):
        char = self.toTest.get_character("Test User")
        char.remove_item("Item A", 1)
        self.toTest.save_data_obj(char)

    def test_06_remove_item_full_from_char(self):
        char = self.toTest.get_character("Test User")
        char.remove_item("Item B")
        self.toTest.save_data_obj(char)

    def test_07_deleted_character(self):
        char = self.toTest.get_character("Test User")
        self.toTest.delete_character(char.name)
        char = self.toTest.get_character("Test User")
        self.assertIsNone(char)

    #
    def test_08_get_character_not_existing(self):
        char = self.toTest.get_character("Somebody Elses Lover")
        self.assertIsNone(char, "Invalid Character get should return none")


# driver code
if __name__ == '__main__':
    unittest.main()
