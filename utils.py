import sys
from time import sleep
import discord
import os

from inspect import getmembers, isfunction

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
    return int(string.lstrip(id_types[strip]["L"]).rstrip(id_types[strip]["R"]))


async def play_sound(voice_client, file):
    source = discord.FFmpegPCMAudio(
        executable=os.path.join(ROOT_DIR, "ffmpeg", "bin", "ffmpeg.exe"),
        source=file)

    voice_client.play(source)

    while voice_client.is_playing():
        sleep(.1)
    await voice_client.disconnect()


async def invalid_args(channel: discord.TextChannel, time: int):
    msg = await channel.send("Invalid argument(s)")
    await msg.delete(delay=time)


def set_exit_handler(func):
    if os.name == "nt":
        try:
            import win32api
            win32api.SetConsoleCtrlHandler(func, True)

        except ImportError:
            version = ".".join(map(str, sys.version_info[:2]))
            raise Exception("pywin32 not installed for Python " + version)
    else:
        pass
        #import signal
        #signal.signal(signal.SIGTERM, func)
        #signal.signal(signal.SIGINT, func)


def get_functions(module):
    return {item[0]: item[1] for item in getmembers(module, isfunction)}
