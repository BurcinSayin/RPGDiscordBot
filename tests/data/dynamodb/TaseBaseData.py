import unittest

import boto3

from data.dynamodb.BaseData import BaseData


class TestCharData(unittest.TestCase):
    def setUp(self):
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

        self.toTest = BaseData(dynamodb, "hebelek")

    def test_init(self):
        self.toTest.get_data_attributes()
