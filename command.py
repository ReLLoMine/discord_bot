import discord

import command_functions


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