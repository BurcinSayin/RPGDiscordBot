from dataclasses import dataclass


@dataclass
class User:
    discord_user_id: str
    active_character: str = ''
    is_admin: int = 0

