from data.sheets.BaseData import BaseData
from data.sheets.Models.User import User


class UserData(BaseData):
    def __init__(self, spreadsheet):
        super().__init__(spreadsheet, "Users")

    def add_user(self, discord_user_id) -> User:
        return self.add_user_row(discord_user_id, '', 0)

    def add_user_row(self, discord_user_id, active_character, is_admin) -> User:
        new_index, new_id = self.insert_row([discord_user_id, active_character, is_admin])
        return self.get_data_obj(User, new_index)

    def get_user(self, discord_user_id):
        user_index = self.find_in_column(2, discord_user_id)
        return self.get_data_obj(User, user_index)

    def get_or_create_user(self, discord_user_id):
        user_index = self.find_in_column(2, discord_user_id)
        if user_index > 0:
            return self.get_data_obj(User, user_index)
        else:
            return self.add_user(discord_user_id)

    #
    # def set_active_char(self, discord_user_id, active_char):
    #     user_index = self.find_in_column(2, discord_user_id)
    #     if user_index > 0:
    #         self.worksheet.update_cell(user_index, 3, active_char)
    #     else:
    #         self.add_user_row(discord_user_id, active_char, 0)
