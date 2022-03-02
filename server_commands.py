from typing import Union, List

from command_processor.command_processor import BaseCommand, BaseCommandProcessor

import utils
import sys
import discord
import server as server_


class ServerCommandProcessor(BaseCommandProcessor):

    def __init__(self, server, **kwargs):
        self.chat_buffer: List[discord.Message] = []
        self.server: server_.Server = server

        kwargs["_input"] = self.chat_input
        kwargs["_output"] = self.chat_output

        self.current_message: discord.Message = None
        self.current_channel: Union[discord.DMChannel, discord.TextChannel] = None
        super().__init__(**kwargs)

    def push_message(self, message):
        self.chat_buffer.append(message)

    def chat_input(self, invite=""):
        message = self.chat_buffer.pop(0)

        self.current_message = message
        self.current_channel = message.channel

        return message.content

    async def chat_output(self, message):
        await self.current_message.channel.send(message)


class ServerCommand(BaseCommand):
    cmdproc: ServerCommandProcessor = None


class Ping(ServerCommand):

    description = "returns 'pong'"

    @classmethod
    async def execute(cls):
        msg = await cls.cmdproc.current_channel.send("pong")
        await msg.delete(delay=5)
        await cls.cmdproc.current_message.delete(delay=5)


async def ping(command, message: discord.Message, args):
    msg = await message.channel.send("pong")
    await msg.delete(delay=5)
    await message.delete(delay=5)


def example_func(command, message: discord.Message, args):
    print(args)

class SetPrefix(ServerCommand):

    description = "changes server prefix"

    @classmethod
    async def execute(cls):
        cls.cmdproc.server.data.prefix = cls.args[0]
        msg = await cls.cmdproc.current_channel.send(f"Now prefix is: {cls.args[0]}")
        await msg.delete(delay=5)
        cls.cmdproc.server.data.save()


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


default_server_commands = {
    "ping": Ping,
    "prefix": SetPrefix
}
