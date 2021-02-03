import discord
import sys

from command import Command
from my_storage import MyStorage, ServerField


def str_to_class(string):
    return getattr(sys.modules[__name__], string)


class Server:

    def __init__(self, client, data: ServerField):
        self.client = client
        self.data = data
        self.commands = {self.data.commands[index].keyname: Command(client, self.data.commands[index]) for index in range(len(self.data.commands))}

    async def try_exec_cmd(self, message: discord.Message):
        cmd, args = self.parse_msg_content(message)

        try:
            print(args)
            await self.commands[cmd].exec(message, args)
        except Exception as exc:
            print(exc)

    def parse_msg_content(self, message: discord.Message):
        """
        :returns cmd_name, *args
        """
        if message.content.startswith(self.data.prefix):
            data = message.content.lstrip(self.data.prefix).split(" ")
        else:
            return None, None

        return data[0], data[1:] if len(data) > 1 else None
