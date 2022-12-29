from data.sheets.Models.BaseInventoryHolder import BaseInventoryHolder


class Organisation(BaseInventoryHolder):
    def __init__(self, index, org_data):
        super().__init__(index, org_data)
        self.inventory = list[org_data]

    @property
    def name(self) -> str:
        return self._current_data[1]

    @name.setter
    def name(self, val: str):
        self._current_data[1] = val

    @property
    def coins(self) -> int:
        return int(self._current_data[2])

    @coins.setter
    def coins(self, val: int):
        self._current_data[2] = val

    @property
    def owner(self) -> str:
        return self._current_data[3]

    @owner.setter
    def owner(self, val: str):
        self._current_data[3] = val
