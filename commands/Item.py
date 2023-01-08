import boto3

from commands.BaseCommand import BaseCommand
from data.dynamodb.CharacterData import CharacterData
from data.dynamodb.UserData import UserData
from utils.discord import InteractionOptionType


class Item(BaseCommand):
    def __init__(self):
        super().__init__("item", "Global item Definitions")
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        self.char_db = CharacterData(dynamodb)
        self.user_db = UserData(dynamodb)

    def get_options(self):
        return [
            {
                "name": "action",
                "description": "global actions for admins",
                "type": InteractionOptionType.STRING.value,
                "required": 1,
                "choices": [
                    {
                        "name": "add",
                        "value": "item_act_add"
                    },
                    {
                        "name": "remove",
                        "value": "item_act_remove"
                    },
                    {
                        "name": "search",
                        "value": "item_act_search"
                    }
                ]
            },
            {
                "name": "item_name",
                "description": "item name",
                "type": InteractionOptionType.STRING.value,
                "required": 1
            },
            {
                "name": "item_data",
                "description": "Comma separated data 'weight, cost, description'",
                "type": InteractionOptionType.STRING.value
            }
        ]

    def process_command(self, body):
        cmd_params = self.get_command_params(body)
        user_id = self.get_user_id(body)
        current_user = self.user_db.get_or_create_user(user_id)
        action_display_name = "Global"
        fields = []
        return_data = {
            "content": ""
        }

        return return_data
