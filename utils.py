import sys
from time import sleep
import discord
import os
from bot import MyClient

ROOT_DIR = sys.path[0]

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


def discord_id(string: str, strip="member"):
    """
    member
    role
    channel
    """
    return int(string.
               lstrip(id_types[strip]["L"]).
               rstrip(id_types[strip]["R"]))


async def play_sound(voice_client, file):
    source = discord.FFmpegPCMAudio(
        executable=os.path.join(ROOT_DIR, "ffmpeg", "bin", "ffmpeg.exe"),
        source=file)

    voice_client.play(source)

    while voice_client.is_playing():
        sleep(.1)
    await voice_client.disconnect()


async def voice_update(client: MyClient, member, before, after):
    server = client.servers[member.guild.id]
    if before.channel is not None and after.channel is not None:
        if before.channel.id == 732177005977534474 and after.afk:
            await member.move_to(before.channel)

    if after.channel is not None:
        if after.channel.category_id == server.data.origin_channel_category:
            channel = await after.channel.clone()
            server.data.created_channels.append(channel.id)
            category = next((x for x in member.guild.categories if x.id == client.servers[
                member.guild.id].data.target_create_channel_category), None)
            await channel.edit(category=category, sync_permissions=True, position=1)
            await member.move_to(channel)

    if before.channel is not None:
        if before.channel.id in server.data.created_channels and len(before.channel.members) == 0:
            server.data.created_channels.remove(before.channel.id)
            await before.channel.delete()
