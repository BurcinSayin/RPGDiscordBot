from data.sheets.Models import InventoryItem
from data.sheets.Models.BaseDataObject import BaseDataObject


class BaseInventoryHolder(BaseDataObject):
    def __init__(self, index, obj_data):
        super().__init__(index, obj_data)
        self.inventory = list[obj_data]

    def find_inventory_item(self, item_name: str) -> InventoryItem:
        ret_val = None
        if len(self.inventory) > 0:
            for item in self.inventory:
                if item.name == item_name:
                    ret_val = item
        return ret_val

    def add_item(self, item_name: str, item_qty: int):
        item_added = False
        target_item = self.find_inventory_item(item_name)
        if target_item is not None:
            item_added = True
            target_item.quantity += item_qty

    def remove_item(self, item_name: str, item_qty: int = 0):
        item_depleted = item_qty == 0
        target_item = self.find_inventory_item(item_name)
        if target_item is not None:
            if item_depleted is not True:
                target_item.quantity -= item_qty
                item_depleted = target_item.quantity <= 0
            if item_depleted:
                target_item.delete_me()
