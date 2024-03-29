import discord

import command_functions
from my_storage import CommandField


class ListMode(enumerate):
    none = 0
    black_list = 1
    white_list = 2


class Command:

    def __init__(self, server, data: CommandField):
        self.client = server.client
        self.server = server
        self.data = data
        self.function = command_functions.get_func(self.data.function)
        self.list_mode = ListMode.none
        list_flag = False

        if len(self.data.channel_whitelist) > 0:
            list_flag = True
            self.list_mode = ListMode.white_list

        if len(self.data.channel_blacklist) > 0:
            if list_flag:
                raise Exception(f"Blacklist/Whitelist error: {self.data}")
            else:
                self.list_mode = ListMode.black_list

    def check_restriction(self, message: discord.Message):
        if self.list_mode == ListMode.none:
            return True

        elif self.list_mode == ListMode.black_list:
            return message.channel.id not in self.data.channel_blacklist

        elif self.list_mode == ListMode.white_list:
            return message.channel.id in self.data.channel_whitelist

    def check_content(self, content):
        raise NotImplementedError

    async def execute(self, message: discord.Message, args):
        if self.check_restriction(message):
            await self.function(self, message, args)
        else:
            await message.delete()
            temp = await message.channel.send("Restricted channel!")
            await temp.delete(delay=10)

    # def log(self):
