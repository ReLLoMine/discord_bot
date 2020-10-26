import discord
import sys

from command import Command


def str_to_class(string):
    return getattr(sys.modules[__name__], string)


class Server:

    def __init__(self, server_id=None,
                 prefix=None,
                 server_dict=None,
                 is_debug=False):

        self.commands = {}
        self.is_debug = is_debug

        if server_dict is not None:
            self.read_from_dict(server_dict)

        if server_id is not None:
            self.server_id = str(server_id)
        if prefix is not None:
            self.prefix = prefix

    def read_from_dict(self, server):
        self.server_id = server["server_id"]
        self.prefix = server["prefix"]
        self.read_from_dict_cmds(server["commands"])

    def read_from_dict_cmds(self, cmds):
        for cmd in cmds:
            self.commands[cmd["keyname"]] = Command(cmd_dict=cmd)

    async def try_exec_cmd(self, message: discord.Message):
        cmd, args = self.parse_msg_content(message)

        try:
            print(args)
            await self.commands[cmd].exec(message, args)
        except Exception as exc:
            print(exc)

    def parse_msg_content(self, message: discord.Message):
        """
        Returns: cmd_name, *args
        """
        if message.content.startswith(self.prefix):
            data = message.content.lstrip(self.prefix).split(" ")
        else:
            return None, None

        return data[0], data[1:] if len(data) > 1 else None
