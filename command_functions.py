import utils
import sys
import discord


async def ping(command, message: discord.Message, args):
    msg = await message.channel.send("pong")
    await msg.delete(delay=5)
    await message.delete(delay=5)

def example_func(command, message: discord.Message, args):
    print(args)

async def set_prefix(command, message: discord.Message, args):
    command.server.prefix = args[0]
    msg = await message.channel.send(f"Now prefix is: {command.client.storage.servers[message.guild.id].prefix}")
    await msg.delete(delay=5)
    command.server.data.save()


async def get_avatar(command, message: discord.Message, args):
    await message.delete()
    await message.channel.send(message.guild.get_member(utils.discord_id(args[0], "member")).avatar_url)

async def set_origin(command, message: discord.Message, args):
    if len(args) == 1:
        try:
            command.server.data.origin_channel_category = int(args[0])
            await message.channel.send("Oki!")
        except ValueError:
            await utils.invalid_args(message.channel, 5)
    else:
        await utils.invalid_args(message.channel, 5)
    await message.delete()
    command.server.data.save()


async def set_target(command, message: discord.Message, args):
    if len(args) == 1:
        try:
            command.server.data.target_create_channel_category = int(args[0])
            await message.channel.send("Oki!")
        except ValueError:
            await utils.invalid_args(message.channel, 5)
    else:
        await utils.invalid_args(message.channel, 5)
    await message.delete()
    command.server.data.save()


async def help_func(command, message: discord.Message, args):
    res = '```\n'
    for cmd in command.server.commands:
        res += f"{cmd} - {command.server.commands[cmd].data.description}\n"
    res += '\n```'
    await message.delete()
    await message.channel.send(res)

def get_func(name: str):
    return getattr(sys.modules[__name__], name)
