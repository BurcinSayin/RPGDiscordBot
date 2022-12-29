import unittest

import gspread

from data.sheets.CharacterData import CharacterData


class TestCharData(unittest.TestCase):

    def setUp(self):
        gc = gspread.service_account(filename='../../../sheet-auth.json')
        char_sheet = gc.open("Characters")
        self.toTest = CharacterData(char_sheet)

    # define a function
    def test_add_character(self):
        char = self.toTest.add_character_row("Test User", 333, 2, 555, "me")
        self.assertEqual("Test User", char.name)
        self.assertEqual(333, char.xp)
        self.assertEqual(2, char.level)
        self.assertEqual(555, char.coins)
        self.assertEqual("me", char.owner)

    def test_get_character(self):
        char = self.toTest.get_character("Test User")
        self.assertEqual("Test User", char.name)

    def test_save_character(self):
        char = self.toTest.get_character("Test User")
        char.coins = 333
        self.toTest.save_data_obj(char)
        char = self.toTest.get_character("Test User")
        self.assertEqual(333, char.coins)

    def test_save_deleted_character(self):
        char = self.toTest.get_character("Test User")
        char.delete_me()
        self.toTest.save_data_obj(char)
        char = self.toTest.get_character("Test User")
        self.assertIsNone(char)

    def test_get_character_not_existing(self):
        char = self.toTest.get_character("Somebody Elses Lover")
        self.assertIsNone(char, "Invalid Character get should return none")

    def test_character_set_id_should_fail(self):
        char = self.toTest.get_character("Husamettin")
        with self.assertRaises(AttributeError):
            char.id = 999

    def test_add_existing_item_to_char(self):
        char = self.toTest.get_character("Husamettin")
        char.add_item("Item A", 5)
        self.toTest.save_data_obj(char)

    def test_remove_existing_item_from_char(self):
        char = self.toTest.get_character("Husamettin")
        char.remove_item("Item A", 1)
        self.toTest.save_data_obj(char)

    def test_add_new_item_to_char(self):
        char = self.toTest.get_character("Husamettin")
        char.add_item("Excalibur", 1)
        self.toTest.save_data_obj(char)

    def test_remove_item_full_from_char(self):
        char = self.toTest.get_character("Husamettin")
        char.remove_item("Excalibur")
        self.toTest.save_data_obj(char)


# driver code
if __name__ == '__main__':
    unittest.main()
