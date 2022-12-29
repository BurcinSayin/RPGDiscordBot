from abc import abstractmethod

from utils.discord import InteractionResponseType


class BaseCommand:
    def __init__(self, name, desc, is_global=False):
        self.command_name = name
        self.command_description = desc
        self.is_global = is_global

    def get_register_json(self):
        reg_json = {
            "name": self.command_name,
            "description": self.command_description
        }

        cmd_options = self.get_options()

        if len(cmd_options) > 0:
            reg_json["options"] = cmd_options

        return reg_json

    def process_event(self, body):
        command_result = self.process_command(body)

        return {
            "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
            "data": command_result
        }

    def process_command(self, body):
        return {
            "content": "RESULT FOR " + self.command_name
        }

    def get_options(self):
        return []

    @staticmethod
    def get_command_params(body):
        cmd_data = body["data"]
        ret_val = {}
        for param in cmd_data["options"]:
            ret_val[param["name"]] = param["value"]

        return ret_val

    @staticmethod
    def get_user_id(body):
        return body["member"]["user"]["id"]

    @staticmethod
    def generate_embed(action, filed_list, color):
        return {
            "type": "rich",
            "title": action,
            "color": color,
            "fields": filed_list
        }
