import command_functions
import discord
import sys


def str_to_class(string):
    return getattr(sys.modules[__name__], string)


class ListMode(enumerate):
    none = 0
    black_list = 1
    white_list = 2


class Command:

    def __init__(self, keyname=None,
                 function=None,
                 cmd_dict=None):

        self.channel_whitelist = []
        self.channel_blacklist = []
        self.list_mode = ListMode.none

        if cmd_dict is not None:
            self.read_from_dict(cmd_dict)

        if keyname is not None:
            self.keyname = keyname
        if function is not None:
            self.function = function

    def check_restriction(self, message: discord.Message):
        if self.list_mode == ListMode.none:
            return True

        elif self.list_mode == ListMode.black_list:
            return message.channel.id not in self.channel_blacklist

        elif self.list_mode == ListMode.white_list:
            return message.channel.id in self.channel_whitelist

    def check_content(self, content):
        raise NotImplementedError

    def read_from_dict(self, command):
        list_flag = False
        self.keyname = command["keyname"]
        self.function = command_functions.get_func(command["function"])

        if len(command["channel_whitelist"]) > 0:
            self.channel_whitelist = command["channel_whitelist"]

            list_flag = True
            self.list_mode = ListMode.white_list

        if len(command["channel_blacklist"]) > 0:
            self.channel_blacklist = command["channel_blacklist"]

            if list_flag:
                raise Exception(f"Blacklist/Whitelist error: {command}")
            else:
                self.list_mode = ListMode.black_list

    async def exec(self, message: discord.Message, args=None):
        if self.check_restriction(message):
            if args is None:
                await self.function(message)
            else:
                await self.function(message, args)
        else:
            await message.channel.send("Неверный канал команды!")


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
