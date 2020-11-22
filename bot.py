#!/usr/bin/python3

import command_functions
from server import *
import discord
import json
import utils
import sys


class MyClient(discord.Client):
    main_channel = 0
    storage_file = None
    token = None
    logfile = None

    def __init__(self):
        super(MyClient, self).__init__()

        file = open("storage.json", "r+")
        self.storage_file = json.loads(file.read())
        file.close()
        self.token = self.storage_file["token"]
        self.owner_id = self.storage_file["owner_id"]

        self.servers = {}
        for server in self.storage_file["servers"]:
            self.servers[server["server_id"]] = Server(server_dict=server)

    async def on_voice_state_update(self, member, before, after):
        await utils.voice_update(self, member, before, after)

    async def on_ready(self):
        game = discord.Activity(type=discord.ActivityType.listening,
                                name="'>>' prefix")
        await self.change_presence(status=discord.Status.online, activity=game)
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.channel.type is discord.ChannelType.private:
            await message.channel.send(message.content)

        elif message.channel.type is discord.ChannelType.text:
            await self.servers[message.guild.id].try_exec_cmd(message)

    def run(self):
        super().run(self.token)


def main():
    client = MyClient()
    client.run()


if __name__ == '__main__':
    main()
