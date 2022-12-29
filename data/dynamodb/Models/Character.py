from dataclasses import dataclass, field

from data.dynamodb.Models.InventoryItem import InventoryItem


@dataclass()
class Character:
    name: str
    xp: int = 0
    level: int = 0
    coins: int = 0
    owner: str = ''
    items: list[InventoryItem] = field(default_factory=list)

    def find_inventory_item(self, item_name: str) -> InventoryItem:
        ret_val = None
        if len(self.items) > 0:
            for item in self.items:
                if item.name == item_name:
                    ret_val = item
        return ret_val

    def add_item(self, item_name: str, item_qty: int):
        item_added = False
        target_item = self.find_inventory_item(item_name)
        if target_item is not None:
            item_added = True
            target_item.quantity += item_qty
        else:
            to_add = InventoryItem(name=item_name, quantity=item_qty)
            self.items.append(to_add)

    def remove_item(self, item_name: str, item_qty: int = 0):
        item_depleted = item_qty == 0
        target_item = self.find_inventory_item(item_name)
        if target_item is not None:
            if item_depleted is not True:
                target_item.quantity -= item_qty
                item_depleted = target_item.quantity <= 0
            if item_depleted:
                self.items.remove(target_item)
