import utils
import sys
import discord


async def ping(command, message: discord.Message):
    msg = await message.channel.send("pong")
    await msg.delete(delay=5)
    await message.delete(delay=5)


def example_func(command, message: discord.Message, args):
    print(args)

async def set_prefix(command, message: discord.Message, args):
    command.client.storage.servers[message.guild.id].prefix = args[0]
    msg = await message.channel.send(f"Now prefix is: {command.client.storage.servers[message.guild.id].prefix}")
    command.client.storage.servers[message.guild.id].save()


async def get_avatar(command, message: discord.Message, args):
    await message.delete()
    await message.channel.send(message.guild.get_member(utils.discord_id(args[0], "member")).avatar_url)


def get_func(name: str):
    return getattr(sys.modules[__name__], name)
