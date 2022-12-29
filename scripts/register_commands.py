import json
import os
import requests

from time import sleep

from dotenv import load_dotenv

from commands import *

load_dotenv()
# discord info, so we know where to publish the slash commands
APPLICATION_ID = os.environ["APPLICATION_ID"]
GUILD_ID = os.environ["GUILD_ID"]

BOT_TOKEN = os.environ["BOT_TOKEN"]
HEADERS = {"Authorization": f"Bot {BOT_TOKEN}"}

# form the APi endpoints: https://discord.com/developers/docs/interactions/slash-commands#registering-a-command
global_url = f"https://discord.com/api/v8/applications/{APPLICATION_ID}/commands"
guild_url = f"https://discord.com/api/v8/applications/{APPLICATION_ID}/guilds/{GUILD_ID}/commands"


def get_json():
    # Opening JSON file
    f = open('../commands/test.json')

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    return data


def publish_command(url, commands):
    r = requests.post(url, headers=HEADERS, json=commands)
    is_success_status = 200 <= r.status_code < 300
    if not is_success_status:
        # pinging the endpoint too frequently causes it to fail; wait and retry
        sleep(20)
        print(f"Post to {url} failed; retrying once")
        r = requests.post(url, headers=HEADERS, json=commands)

    # debug print
    print(f"Response from {url}: {r.text}")


def get_all_commands(url):
    existing_commands = requests.get(url, headers=HEADERS).json()
    if not existing_commands:
        return []
    return existing_commands


def delete_command(url):
    r = requests.delete(url, headers=HEADERS)
    print(f"Delete response: {r.status_code}")


def run():
    # use guild_urls to test, since global changes take effect after a delay
    # optional: delete all existing commands to reset to clean state
    # for guild_url in guild_urls:
    for dev_command in get_all_commands(guild_url):
        sleep(5)
        delete_command(f"{guild_url}/{dev_command['id']}")
    #
    # for glb_command in get_all_commands(global_url):
    #     sleep(5)
    #     delete_command(f"{global_url}/{glb_command['id']}")

    # publish new commands
    for cmd in commands_list:
        print(commands_list[cmd].get_register_json())
        publish_command(guild_url, commands_list[cmd].get_register_json())
        print(f"{cmd} command published")


if __name__ == "__main__":
    run()
