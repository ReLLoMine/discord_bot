from typing import List

import discord
import sys

import utils
from command import Command
from my_storage import MyStorage, ServerField


def str_to_class(string):
    return getattr(sys.modules[__name__], string)


class Server:

    def __init__(self, client, data: ServerField, def_commands=True):
        self.client = client
        self.data = data
        if def_commands:
            self.commands: List[Command] = {
                self.client.storage.default_commands[index].keyname:
                    Command(self, self.client.storage.default_commands[index])
                for index in range(len(self.client.storage.default_commands))
            }
        else:
            self.commands: List[Command] = {
                self.data.commands[index].keyname:
                    Command(self, self.data.commands[index])
                for index in range(len(self.data.commands))
            }

    async def try_exec_cmd(self, message: discord.Message):
        cmd, args = self.parse_msg_content(message)
        print(args)

        if cmd:
            try:
                await self.commands[cmd].execute(message, args)
            except Exception as exc:
                print(exc)
                await message.delete()
                await utils.invalid_args(message.channel, 5)

    def parse_msg_content(self, message: discord.Message):
        """
        :returns cmd_name, *args
        """
        if message.content.startswith(self.data.prefix):
            data = message.content.lstrip(self.data.prefix).split(" ")
        else:
            return None, None

        return data[0], data[1:] if len(data) > 1 else None

    def is_prefix_help(self, message: discord.Message):
        pass