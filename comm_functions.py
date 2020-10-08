import sys
import discord


def discord_id(string: str, tpid="member"):
    types = {
        "member": {
            "left": "<@!",
            "right": ">"
        },
        "role": {
            "left": "<@&",
            "right": ">"
        },
        "channel": {
            "left": "<#",
            "right": ">"
        }
    }
    return int(string.lstrip(types[tpid]["left"]).rstrip(types[tpid]["right"]))
