#!/usr/bin/python3

from server import *
import discord
import my_storage

# Modules
from modules import *


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

        utils.set_exit_handler(self.on_exit)
    #     self.load_functions()
    #
    # def load_functions(self):
    #     for module_ in modules.sub_modules():
    #         self.__dict__.update(utils.get_functions(module_))

    async def on_message_edit(self, before, after):
        await runtime.on_message_edit(self, before, after)

    async def on_message_delete(self, message):
        await runtime.on_message_delete(self, message)

    async def on_typing(self, channel, user, when):
        await runtime.on_typing(self, channel, user, when)

    async def on_voice_state_update(self, member, before, after):
        await voice.on_voice_state_update(self, member, before, after)

    async def on_ready(self):
        await on_start.on_ready(self)

    async def check_avaiable_servers(self):
        await on_start.check_avaiable_servers(self)

    async def on_message(self, message):
        await runtime.on_message(self, message)

    async def on_guild_join(self, guild):
        await runtime.on_guild_join(self, guild)

    @staticmethod
    def reload_modules():
        importlib.reload(modules)

    def run(self):
        super().run(self.storage.token)

    def on_exit(self, sig, func=None):
        self.storage.save()


def main():
    client = MyClient()
    client.run()


if __name__ == '__main__':
    main()
