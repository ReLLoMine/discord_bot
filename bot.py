#!/usr/bin/python3

import command_functions
from server import *
import discord
import utils
import my_storage

class MyClient(discord.Client):
    logfile = None

    def __init__(self):
        super(MyClient, self).__init__()
        self.storage = my_storage.MyStorage()
        self.servers = {int(self.storage.servers[index].server_id): Server(self.storage.servers[index]) for index in range(len(self.storage.servers))}

    async def on_voice_state_update(self, member, before, after):
        await utils.voice_update(self, member, before, after)

    async def on_ready(self):
        game = discord.Activity(type=discord.ActivityType.listening,
                                name="'>>' prefix")
        await self.change_presence(status=discord.Status.online, activity=game)
        print('Logged on as', self.user)

        for server in self.storage.servers:
            guild = self.get_guild(server.server_id)
            for channel in server.created_channels:
                _channel = guild.get_channel(channel)
                if len(_channel.members) == 0:
                    server.created_channels.remove(_channel.id)
                    await _channel.delete()

        self.storage.save()

    async def on_message(self, message: discord.Message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.channel.type is discord.ChannelType.private:
            await message.channel.send(message.content)

        elif message.channel.type is discord.ChannelType.text:
            await self.servers[message.guild.id].try_exec_cmd(message)

    def run(self):
        super().run(self.storage.token)


def main():
    client = MyClient()
    client.run()


if __name__ == '__main__':
    main()
