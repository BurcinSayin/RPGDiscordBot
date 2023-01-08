import unittest

import boto3

from data.dynamodb.ItemData import ItemData


class TestItemData(unittest.TestCase):
    def setUp(self):
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        self.toTest = ItemData(dynamodb)

    def test_01_add_item(self):
        item = self.toTest.add_item("test item name", 1, 2, "test description")
        self.assertIsNotNone(item)
        self.assertEqual(item.name, "test item name")

    def test_02_get_item(self):
        item = self.toTest.get_item("test item name")
        self.assertIsNotNone(item)
        self.assertEqual(item.name, "test item name")
        self.assertEqual(item.description, "test description")
