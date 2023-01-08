import boto3

from commands.BaseCommand import BaseCommand
from data.dynamodb.ItemData import ItemData
from data.dynamodb.UserData import UserData
from utils.discord import InteractionOptionType


class Item(BaseCommand):
    def __init__(self):
        super().__init__("item", "Global item Definitions")
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        self.user_db = UserData(dynamodb)
        self.item_db = ItemData(dynamodb)

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
                "type": InteractionOptionType.STRING.value,
                "required": 0
            }
        ]

    def process_command(self, body):
        cmd_params = self.get_command_params(body)
        user_id = self.get_user_id(body)
        current_user = self.user_db.get_or_create_user(user_id)
        action_display_name = "Item"
        fields = []
        return_data = {
            "content": ""
        }

        if current_user.is_admin <= 0:
            fields.append({"name": "Auth Error", "value": "You Should be Admin"})
        else:
            action_param = cmd_params.get("action")
            item_name = cmd_params.get("item_name")
            if action_param == "item_act_add":
                item_data = [0, 0, '']
                item_data_str = cmd_params.get("item_data")
                if item_data_str is not None and ',' in item_data_str:
                    if len(item_data_str.split(',')) > 2:
                        item_data = item_data_str.split(',')
                action_display_name = "Item Add"
                added_item = self.item_db.add_item(item_name, int(item_data[0]), int(item_data[1]),
                                                   item_data[2])
                self.append_item_fields(added_item, fields)

            if action_param == "item_act_remove":
                action_display_name = "Item Remove"
                self.item_db.delete_item(item_name)
                fields.append({"name": "Item Deleted", "value": item_name})

            if action_param == "item_act_search":
                action_display_name = "Item Search"
                found_item = self.item_db.get_item(item_name)
                if found_item is None:
                    fields.append({"name": "Item Not Found", "value": ""})
                else:
                    self.append_item_fields(found_item, fields)

        return_data["embeds"] = [self.generate_embed(action_display_name, fields, 0x89ff0a)]
        return return_data

    def append_item_fields(self, added_item, fields):
        fields.append({"name": "Name", "value": added_item.name, "inline": True})
        fields.append({"name": "Cost", "value": added_item.cost, "inline": True})
        fields.append({"name": "Weight", "value": added_item.weight, "inline": True})
        fields.append({"name": "Description", "value": added_item.description, "inline": True})
