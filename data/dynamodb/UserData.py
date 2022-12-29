from dataclasses import asdict

from data.dynamodb.BaseData import BaseData
from data.dynamodb.Models.User import User


class UserData(BaseData):
    def __init__(self, db):
        super().__init__(db, "users", "discord_user_id", "S")

    def add_user(self, user_id) -> User:
        to_add = User(discord_user_id=user_id)
        save_data = asdict(to_add)

        self.table.put_item(
            Item=save_data
        )
        return to_add

    def delete_user(self, user_id: str):
        self.table.delete_item(
            Key={
                self.key_attribute_name: user_id
            }
        )

    def get_user(self, user_id) -> User:
        response = self.table.get_item(
            Key={
                self.key_attribute_name: user_id
            }
        )
        db_data = response.get('Item')
        if db_data is None:
            return None

        char_data = User(**db_data)
        return char_data

    def get_or_create_user(self, user_id):
        existing_user = self.get_user(user_id)
        if existing_user is None:
            return self.add_user(user_id)
        else:
            return existing_user


