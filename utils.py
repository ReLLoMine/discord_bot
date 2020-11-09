import sys
from time import sleep

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


def discord_id(string: str, str_type="member"):
    """
    member
    role
    channel
    """
    return int(string.
               lstrip(id_types[str_type]["L"]).
               rstrip(id_types[str_type]["R"]))


async def play_sound(voice_client, file):
    source = discord.FFmpegPCMAudio(
        executable="ffmpeg\\bin\\ffmpeg.exe",
        source=file)

    voice_client.play(source)

    while voice_client.is_playing():
        sleep(.1)
    await voice_client.disconnect()


async def voice_update(self, member, before, after):
    if member.id == self.owner_id:
        if before.channel is not None and after.channel is not None:
            if before.channel.id == 732177005977534474 and \
                    after.afk:
                await member.move_to(before.channel)
    elif member.id == 319529608292728836:
        if after.channel is not None:
            voice_client = await after.channel.connect()
            await play_sound(voice_client, "sounds\\3.14др.m4a")
