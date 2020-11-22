import utils
import sys
import discord


async def ping(message: discord.Message):
    await message.channel.send("pong")


def example_func(message: discord.Message, args):
    print(args)


async def get_avatar(message: discord.Message, args):
    await message.delete()
    await message.channel.send(message.guild.get_member(utils.discord_id(args[0], "member")).avatar_url)


def get_func(name: str):
    return getattr(sys.modules[__name__], name)
