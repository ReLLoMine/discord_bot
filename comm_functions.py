import sys
import discord

id_types = {
    "member": {
        "L": "<@!",
        "R": ">"
    },
    "role": {
        "L": "<@&",
        "R": ">"
    },
    "channel": {
        "L": "<#",
        "R": ">"
    }
}


def discord_id(string: str, tpid="member"):
    """
    member
    role
    channel
    """

    return int(string.lstrip(id_types[tpid]["L"]).rstrip(id_types[tpid]["R"]))
