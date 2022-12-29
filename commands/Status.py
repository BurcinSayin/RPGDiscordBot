import os

import boto3
import gspread

from commands.BaseCommand import BaseCommand
from data.dynamodb.CharacterData import CharacterData
from data.dynamodb.Models import Character, User
from data.dynamodb.UserData import UserData


class Status(BaseCommand):
    def __init__(self):
        super().__init__("status", "Get Current status info")
        # sheet_auth_file = "../sheet-auth.json"
        # sheet_auth_path = os.environ.get("SHEET_PATH")
        # if sheet_auth_path is not None:
        #     sheet_auth_file = str(sheet_auth_path) + "sheet-auth.json"
        # gc = gspread.service_account(filename=sheet_auth_file)
        # settings_sheet = gc.open("Settings")
        # char_sheet = gc.open("Characters")
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        self.char_db = CharacterData(dynamodb)
        self.user_db = UserData(dynamodb)

    def process_command(self, body):
        user_id = self.get_user_id(body)
        current_user = self.user_db.get_or_create_user(user_id)
        active_char = self.char_db.get_character(current_user.active_character)
        embeds = [self.get_user_status_embed(current_user)]
        if active_char is not None:
            embeds.append(self.get_active_char_embed(active_char))

        return {
            "content": "",
            "embeds": embeds
        }

    def get_user_status_embed(self, current_user: User):
        fields = [{"name": f"Discord UserId", "value": str(current_user.discord_user_id), "inline": "true"},
                  {"name": f"Is Admin", "value": current_user.is_admin, "inline": "true"}]
        return self.generate_embed("User Status", fields, 0x4681d3)

    def get_active_char_embed(self, active_char: Character):
        fields = [
            {"name": f"Name", "value": active_char.name, "inline": "true"},
            {"name": f"Coins", "value": str(active_char.coins), "inline": "true"},
            {"name": f"XP", "value": str(active_char.xp), "inline": "true"},
            {"name": f"Level", "value": str(active_char.level), "inline": "true"}
        ]
        return self.generate_embed("Active Character", fields, 0xd3be46)


