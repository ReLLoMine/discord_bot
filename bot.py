#!/usr/bin/python3
from copy import copy

import command_functions
from server import *
import discord
import utils
import my_storage

class MyClient(discord.Client):
    intents = discord.Intents.default()
    intents.members = True
    logfile = None

    def __init__(self):
        super(MyClient, self).__init__(intents=self.intents)
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
                if _channel is not None and len(_channel.members) == 0:
                    await _channel.delete()
                    server.created_channels.remove(_channel.id)
                elif _channel is None:
                    server.created_channels.remove(channel)

        self.storage.save()

    async def on_message(self, message: discord.Message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.channel.type is discord.ChannelType.private:
            await message.channel.send(message.content)

        elif message.channel.type is discord.ChannelType.text:
            await self.servers[message.guild.id].try_exec_cmd(message)

    async def on_guild_join(self, guild: discord.Guild):
        server = ServerField()
        server.server_id = guild.id
        server.commands = copy(self.storage.default_commands)
        self.storage.servers.append(server)
        self.servers[guild.id] = Server(server)
        self.storage.save()

    def run(self):
        super().run(self.storage.token)


def main():
    client = MyClient()
    client.run()


if __name__ == '__main__':
    main()
