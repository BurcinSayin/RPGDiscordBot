from dataclasses import asdict

from data.dynamodb.BaseData import BaseData
from data.dynamodb.Models.Character import Character
from data.dynamodb.Models.GlobalItem import GlobalItem


class ItemData(BaseData):
    def __init__(self, db):
        super().__init__(db, "items", "name", "S")

    def add_item(self, character_name, weight, cost, desc) -> GlobalItem:
        to_save = GlobalItem(name=character_name, weight=weight, cost=cost, description=desc)
        save_data = asdict(to_save)

        self.table.put_item(
            Item=save_data
        )
        return to_save

    def delete_item(self, item_name: str):
        self.table.delete_item(
            Key={
                self.key_attribute_name: item_name
            }
        )

    def get_item(self, item_name) -> GlobalItem:
        if item_name is None or item_name == '':
            return None
        response = self.table.get_item(
            Key={
                self.key_attribute_name: item_name
            }
        )
        db_data = response.get('Item')
        if db_data is None:
            return None

        item_data = GlobalItem(**db_data)
        return item_data
