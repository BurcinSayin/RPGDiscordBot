import json
import os

from nacl.signing import VerifyKey
from commands import *
from utils.discord import InteractionResponseType, InteractionType

PING_PONG = {"type": 1}


def verify_signature(event):
    public_key = os.environ.get("PUBLIC_KEY")
    raw_body = event.get("body")
    auth_sig = event['headers'].get('x-signature-ed25519')
    auth_ts = event['headers'].get('x-signature-timestamp')

    message = auth_ts.encode() + raw_body.encode()
    verify_key = VerifyKey(bytes.fromhex(public_key))
    verify_key.verify(message, bytes.fromhex(auth_sig))  # raises an error if unequal


def ping_pong(body):
    if body.get("type") == 1:
        return True
    return False


def lambda_handler(event, context):
    print(f"event {event}")  # debug print
    # verify the signature
    try:
        verify_signature(event)
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")

    # check if message is a ping
    body = json.loads(event.get('body'))
    interaction_type = body.get("type")
    if interaction_type == InteractionType.PING.value:
        return {"type": InteractionResponseType.PONG.value}

    if interaction_type == InteractionType.APPLICATION_COMMAND.value:
        command_name = body["data"]["name"]
        handled_event_response = commands_list[command_name].process_event(body)
        print(f"response {handled_event_response}")  # debug print
        return handled_event_response

    # dummy return
    return {
        "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
        "data": {
            "content": "BEEP BOOP"
        }
    }
