import sys
import discord


async def ping(message: discord.Message):
    await message.channel.send("pong")


def example_func(message: discord.Message, args):
    print(args)


async def add_role(message: discord.Message, args):
    await message.guild.create_role()


def get_func(name: str):
    return getattr(sys.modules[__name__], name)
