from data.sheets.Models.BaseDataObject import BaseDataObject


class InventoryItem(BaseDataObject):

    @property
    def holder_name(self) -> str:
        return self._current_data[1]

    @holder_name.setter
    def holder_name(self, val: str):
        self._current_data[1] = val

    @property
    def name(self) -> str:
        return self._current_data[2]

    @name.setter
    def name(self, val: str):
        self._current_data[2] = val

    @property
    def quantity(self) -> int:
        return int(self._current_data[3])

    @quantity.setter
    def quantity(self, val: int):
        self._current_data[3] = val
