import os

import boto3

from commands.BaseCommand import BaseCommand
from data.dynamodb.Models.Character import Character
from data.dynamodb.Models.User import User

from data.dynamodb.UserData import UserData
from data.dynamodb.CharacterData import CharacterData

from utils.discord import InteractionOptionType


class Char(BaseCommand):
    def __init__(self):
        super().__init__("char", "Character actions")
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        self.char_db = CharacterData(dynamodb)
        self.user_db = UserData(dynamodb)

    def get_options(self):
        return [
            {
                "name": "action",
                "description": "character action",
                "type": InteractionOptionType.STRING.value,
                "required": 1,
                "choices": [
                    {
                        "name": "Create",
                        "value": "char_act_create"
                    },
                    {
                        "name": "Switch",
                        "value": "char_act_switch"
                    },
                    {
                        "name": "List",
                        "value": "char_act_list"
                    }
                ]
            },
            {
                "name": "char_name",
                "description": "Character Name",
                "type": InteractionOptionType.STRING.value,
                "required": 0
            }
        ]

    def process_command(self, body):
        cmd_params = self.get_command_params(body)
        user_id = self.get_user_id(body)
        current_user = self.user_db.get_or_create_user(user_id)
        fields = []
        action_display_name = "Unknown"
        return_data = {
            "content": ""
        }

        char_name_param = cmd_params.get("char_name")
        action_param = cmd_params.get("action")

        if action_param == "char_act_create":
            action_display_name = "Create Char"
            if char_name_param is None:
                fields.append({"name": "Param Error", "value": "char_name required"})
            # current_char = self.entity_db.get_entity(guild_id, char_name_param, "C")
            current_char = self.char_db.get_character(char_name_param)
            if current_char is None:
                # created_id = self.entity_db.add_entity(guild_id, user_id, char_name_param, "C")
                self.char_db.add_character(char_name_param, current_user.discord_user_id)
                fields.append({"name": "New character created", "value": char_name_param})
                # created_char = self.entity_db.get_entity(guild_id, char_name_param, "C")
                created_char = self.char_db.get_character(char_name_param)
                fields.append(self.switch_entity(created_char, current_user))
            else:
                fields.append({"name": "Already Exists", "value": current_char.name})
                fields.append(self.switch_entity(current_char, current_user))

        if action_param == "char_act_list":
            action_display_name = "Character List"
            char_list = self.char_db.get_all()
            for found_char in char_list:
                fields.append({"name": "Char:", "value": found_char.name})

        if action_param == "char_act_switch":
            action_display_name = "Switch Char"
            # target_char = self.entity_db.get_entity(guild_id, char_name_param, "C")
            target_char = self.char_db.get_character(char_name_param)
            fields.append(self.switch_entity(target_char, current_user))

        return_data["embeds"] = [self.generate_embed(action_display_name, fields, 0x89ff0a)]

        return return_data

    def switch_entity(self, target_char: Character, current_user: User):
        if target_char is not None:
            if current_user.discord_user_id in target_char.owner:
                current_user.active_character = target_char.name
                self.user_db.save_data_obj(current_user)
                return {"name": "Switched to Char", "value": target_char.name}
            else:
                return {"name": "Cannot Switch", "value": "Different owner"}
        else:
            return {"name": "Cannot Switch", "value": "Character not found"}
