from data.sheets.Models.BaseInventoryHolder import BaseInventoryHolder


class Character(BaseInventoryHolder):
    def __init__(self, index, char_data):
        super().__init__(index, char_data)

    @property
    def name(self) -> str:
        return self._current_data[1]

    @name.setter
    def name(self, val: str):
        self._current_data[1] = val

    @property
    def xp(self) -> int:
        return int(self._current_data[2])

    @xp.setter
    def xp(self, val: int):
        self._current_data[2] = val

    @property
    def level(self) -> int:
        return int(self._current_data[3])

    @level.setter
    def level(self, val: int):
        self._current_data[3] = val

    @property
    def coins(self) -> int:
        return int(self._current_data[4])

    @coins.setter
    def coins(self, val: int):
        self._current_data[4] = val

    @property
    def owner(self) -> str:
        return self._current_data[5]

    @owner.setter
    def owner(self, val: str):
        self._current_data[5] = val

    # def find_inventory_item(self, item_name: str) -> InventoryItem:
    #     ret_val = None
    #     if len(self.inventory) > 0:
    #         for item in self.inventory:
    #             if item.name == item_name:
    #                 ret_val = item
    #     return ret_val
    #
    # def add_item(self, item_name: str, item_qty: int):
    #     item_added = False
    #     target_item = self.find_inventory_item(item_name)
    #     if target_item is not None:
    #         item_added = True
    #         target_item.quantity += item_qty
    #
    # def remove_item(self, item_name: str, item_qty: int = 0):
    #     item_depleted = item_qty == 0
    #     target_item = self.find_inventory_item(item_name)
    #     if target_item is not None:
    #         if item_depleted is not True:
    #             target_item.quantity -= item_qty
    #             item_depleted = target_item.quantity <= 0
    #         if item_depleted:
    #             target_item.delete_me()
