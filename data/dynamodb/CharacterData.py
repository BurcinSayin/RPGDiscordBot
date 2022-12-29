from dataclasses import asdict

from data.dynamodb.BaseData import BaseData
from data.dynamodb.Models.Character import Character
from data.dynamodb.Models.InventoryItem import InventoryItem


def _map_to_model(data: dict):
    ret_val = Character(**data)
    if len(ret_val.items) > 0:
        mapped_inventory = list()
        for inv_item_data in ret_val.items:
            mapped_inventory.append(InventoryItem(**inv_item_data))
        ret_val.items = mapped_inventory
    return ret_val


class CharacterData(BaseData):
    def __init__(self, db):
        super().__init__(db, "characters", "name", "S")

    def add_character(self, character_name, owner) -> Character:
        to_save = Character(name=character_name, owner=owner)
        save_data = asdict(to_save)

        self.table.put_item(
            Item=save_data
        )
        return to_save

    def delete_character(self, character_name: str):
        self.table.delete_item(
            Key={
                self.key_attribute_name: character_name
            }
        )

    def get_character(self, name) -> Character:
        if name is None or name == '':
            return None
        response = self.table.get_item(
            Key={
                self.key_attribute_name: name
            }
        )
        db_data = response.get('Item')
        if db_data is None:
            return None

        return _map_to_model(db_data)

    def get_all(self):
        ret_val = list()
        response = self.table.scan()
        data_list = response['Items']
        for item_data in data_list:
            ret_val.append(_map_to_model(item_data))

        return ret_val
