from data.sheets.Models.BaseDataObject import BaseDataObject


class User(BaseDataObject):
    # id	discord_user_id	active_character	is_admin

    @property
    def discord_user_id(self) -> str:
        return self._current_data[1]

    @discord_user_id.setter
    def discord_user_id(self, val):
        self._current_data[1] = val

    @property
    def active_character(self) -> str:
        return self._current_data[2]

    @active_character.setter
    def active_character(self, val):
        self._current_data[2] = val

    @property
    def is_admin(self) -> int:
        return int(self._current_data[3])

    @is_admin.setter
    def is_admin(self, val: int):
        self._current_data[3] = val
