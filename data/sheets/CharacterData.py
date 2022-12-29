from data.sheets.BaseData import BaseData
from data.sheets.Models.Character import Character
from data.sheets.Models.InventoryItem import InventoryItem


class CharacterData(BaseData):
    def __init__(self, spreadsheet):
        super().__init__(spreadsheet, "Main")
        self.add_sub_sheet("Inventory", 2)

    def add_character(self, character_name, owner_id) -> Character:
        return self.add_character_row(character_name, 0, 1, 0, owner_id)

    def add_character_row(self, name, xp, level, coins, owner) -> Character:
        new_index, new_id = self.insert_row([name, xp, level, coins, owner])
        return self.get_data_obj(Character, new_index)

    def get_character(self, name) -> Character:
        char_index = self.find_in_column(2, name)
        ret_val = self.get_data_obj(Character, char_index)
        if ret_val is not None:
            ret_val.inventory = self.get_sub_data_obj_list("Inventory", InventoryItem, name)
        return ret_val

    def save_data_obj(self, data_obj: Character):
        sub_sheet, col_ref = self.get_sub_sheet_or_default("Inventory")
        if sub_sheet is not None:
            for item in data_obj.inventory:
                self.save_simple_data_obj(item, sub_sheet)
        self.save_simple_data_obj(data_obj)
        pass


