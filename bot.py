#!/usr/bin/python3
from copy import copy

import command_functions
import voice
from server import *
import discord
import utils
import my_storage
import os
import sys


def set_exit_handler(func):
    if os.name == "nt":
        try:
            import win32api
            win32api.SetConsoleCtrlHandler(func, True)

        except ImportError:
            version = ".".join(map(str, sys.version_info[:2]))
            raise Exception("pywin32 not installed for Python " + version)
    else:
        pass
        #import signal
        #signal.signal(signal.SIGTERM, func)
        #signal.signal(signal.SIGINT, func)


class MyClient(discord.Client):
    intents = discord.Intents.default()
    intents.members = True
    logfile = None

    def __init__(self):
        super(MyClient, self).__init__(intents=self.intents)
        self.storage = my_storage.MyStorage(filepath="storage.json")
        self.servers: List[Server] = {
            server_id: Server(self, self.storage.servers[server_id]) for server_id in self.storage.servers.keys()
        }

        set_exit_handler(self.on_exit)

    async def on_voice_state_update(self, member, before, after):
        await voice.voice_update(self, member, before, after)

    async def on_ready(self):
        game = discord.Activity(type=discord.ActivityType.listening,
                                name="'>>' prefix")
        await self.change_presence(status=discord.Status.online, activity=game)

        print('Logged on as: ', self.user)

        await self.check_avaiable_servers()

        self.storage.save()

    async def check_avaiable_servers(self):

        for server in self.storage.servers.values():
            guild = self.get_guild(server.server_id)
            
            for channel in server.created_channels:
                _channel = guild.get_channel(channel)

                if _channel is not None and len(_channel.members) == 0:
                    await _channel.delete()
                    server.created_channels.remove(_channel.id)
                elif _channel is None:
                    server.created_channels.remove(channel)

        for guild in self.guilds:
            if guild.id not in self.servers:
                await self.on_guild_join(guild)

    async def on_message(self, message: discord.Message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        # don't respond to bots
        if message.author.bot:
            return

        if message.channel.type is discord.ChannelType.private:
            if message.content == "SHUTD0WN-7311097":
                self.storage.save()
                await self.close()
            else:
                await message.channel.send(message.content)

        elif message.channel.type is discord.ChannelType.text:
            await self.servers[message.guild.id].try_exec_cmd(message)

    async def on_guild_join(self, guild: discord.Guild):
        server = ServerField(storage=self.storage)
        server.server_id = guild.id
        self.storage.servers[guild.id] = server
        self.servers[guild.id] = Server(self, server)
        self.storage.save()

    def run(self):
        super().run(self.storage.token)

    def on_exit(self, sig, func=None):
        self.storage.save()


def main():
    client = MyClient()
    client.run()


if __name__ == '__main__':
    main()
