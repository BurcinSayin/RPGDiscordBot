import unittest

import gspread

from data.sheets.OrganisationData import OrganisationData


class TestOrgData(unittest.TestCase):

    def setUp(self):
        gc = gspread.service_account(filename='../../../sheet-auth.json')
        char_sheet = gc.open("Organisations")
        self.toTest = OrganisationData(char_sheet)

    # define a function
    def test_add_organisation(self):
        org = self.toTest.add_organisation_row("Test Org", 555, "me")
        self.assertEqual("Test Org", org.name)
        self.assertEqual(555, org.coins)
        self.assertEqual("me", org.owner)

    def test_get_organisation(self):
        org = self.toTest.get_organisation("Test Org")
        self.assertEqual("Test Org", org.name)

    def test_save_organisation(self):
        org = self.toTest.get_organisation("Test Org")
        org.coins = 333
        self.toTest.save_data_obj(org)
        org = self.toTest.get_organisation("Test Org")
        self.assertEqual(333, org.coins)

    def test_save_organisation_deleted(self):
        org = self.toTest.get_organisation("Test Org")
        org.delete_me()
        self.toTest.save_data_obj(org)
        deleted_org = self.toTest.get_organisation("Test Org")
        self.assertIsNone(deleted_org)

    def test_get_organisation_not_existing(self):
        org = self.toTest.get_organisation("Somebody Elses Lover")
        self.assertIsNone(org, "Invalid Character get should return none")

    def test_organisation_set_id_should_fail(self):
        org = self.toTest.get_organisation("Upright Barristers")
        with self.assertRaises(AttributeError):
            org.id = 999

    def test_add_existing_item_to_org(self):
        org = self.toTest.get_organisation("Upright Barristers")
        org.add_item("Item A", 5)
        self.toTest.save_data_obj(org)

    def test_remove_existing_item_from_org(self):
        org = self.toTest.get_organisation("Upright Barristers")
        org.remove_item("Item A", 1)
        self.toTest.save_data_obj(org)

    def test_add_new_item_to_org(self):
        org = self.toTest.get_organisation("Upright Barristers")
        org.add_item("Excalibur", 1)
        self.toTest.save_data_obj(org)

    def test_remove_item_full_from_org(self):
        org = self.toTest.get_organisation("Upright Barristers")
        org.remove_item("Excalibur")
        self.toTest.save_data_obj(org)


# driver code
if __name__ == '__main__':
    unittest.main()
