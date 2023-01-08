import os

import boto3
import gspread

from commands.BaseCommand import BaseCommand
from data.dynamodb.CharacterData import CharacterData
from data.dynamodb.Models.User import User
from data.dynamodb.UserData import UserData
from utils.coin import parse_coin_string, create_coin_string
from utils.discord import InteractionOptionType


class Coin(BaseCommand):
    def __init__(self):
        super().__init__("coin", "Trading coins")
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        self.char_db = CharacterData(dynamodb)
        self.user_db = UserData(dynamodb)


    def get_options(self):
        return [
            {
                "name": "action",
                "description": "coin action (add,remove is for admins)",
                "type": InteractionOptionType.STRING.value,
                "required": 1,
                "choices": [
                    {
                        "name": "give",
                        "value": "coin_act_give"
                    },
                    {
                        "name": "add",
                        "value": "coin_act_add"
                    },
                    {
                        "name": "remove",
                        "value": "coin_act_remove"
                    }
                ]
            },
            {
                "name": "coin_target",
                "description": "Target character name",
                "type": InteractionOptionType.STRING.value,
                "required": 1
            },
            {
                "name": "coin_amount",
                "description": "Coin Amount. Example: '1pp 100gp 50sp 3cp'",
                "type": InteractionOptionType.STRING.value,
                "required": 1
            }
        ]

    def process_command(self, body):
        cmd_params = self.get_command_params(body)
        user_id = self.get_user_id(body)
        current_user = self.user_db.get_or_create_user(user_id)
        action_display_name = "Coins"
        fields = []
        return_data = {
            "content": ""
        }

        coin_target_param = cmd_params.get("coin_target")
        coin_target = self.char_db.get_character(coin_target_param)
        if coin_target is None:
            fields.append({"name": "Param Error", "value": "Coin target cant be found"})
            return_data["embeds"] = [self.generate_embed(action_display_name, fields, 0x89ff0a)]
            return return_data

        action_param = cmd_params.get("action")
        coin_source = self.get_coin_source(current_user)
        coin_amount = parse_coin_string(cmd_params.get("coin_amount"))

        if action_param == "coin_act_give":
            action_display_name = "Coin Give"
            if coin_source.coins < coin_amount:
                fields.append({"name": "Param Error", "value": f"{coin_source.name} does not have enough coins"})
                return_data["embeds"] = [self.generate_embed(action_display_name, fields, 0x89ff0a)]
                return return_data

            coin_source.coins -= coin_amount
            coin_target.coins += coin_amount
            self.char_db.save_data_obj(coin_source)
            self.char_db.save_data_obj(coin_target)
            fields.append({"name": f"{coin_source.name} Coins", "value": create_coin_string(coin_source.coins)})
            fields.append({"name": f"{coin_target.name} Coins", "value": create_coin_string(coin_target.coins)})

        if action_param == "coin_act_add":
            action_display_name = "Coin Add"
            if current_user.is_admin <= 0:
                fields.append({"name": "Auth Error", "value": "You Should be Admin"})
            else:
                coin_target.coins += coin_amount
                self.char_db.save_data_obj(coin_target)
                fields.append({"name": f"{coin_target.name} Coins", "value": create_coin_string(coin_target.coins)})

        if action_param == "coin_act_remove":
            action_display_name = "Coin Remove"
            if current_user.is_admin <= 0:
                fields.append({"name": "Auth Error", "value": "You Should be Admin"})
                return return_data
            else:
                coin_target.coins -= coin_amount
                self.char_db.save_data_obj(coin_target)
                fields.append({"name": f"{coin_target.name} Coins", "value": create_coin_string(coin_target.coins)})

        return_data["embeds"] = [self.generate_embed(action_display_name, fields, 0x89ff0a)]
        return return_data

    def get_coin_source(self, active_user: User):
        if active_user is not None:
            return self.char_db.get_character(active_user.active_character)
        else:
            return None

