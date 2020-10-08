import command_functions
from server import *
import discord
import json
import sys


class MyClient(discord.Client):
    main_channel = 0
    storage_file = None
    token = None

    def __init__(self):
        super(MyClient, self).__init__()

        file = open("storage.json", "r+")
        self.storage_file = json.loads(file.read())
        file.close()
        self.token = self.storage_file["token"]

        self.servers = {}
        for server in self.storage_file["servers"]:
            self.servers[server["server_id"]] = Server(server_dict=server)

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.channel.type is discord.ChannelType.private:
            pass
        elif message.channel.type is discord.ChannelType.text:
            await self.servers[message.guild.id].try_exec_cmd(message)


def main():
    # discord.message.Message.content
    # game = discord.Game("with the API")
    # client.change_presence(status=discord.Status.idle, activity=game)

    client = MyClient()
    client.run(client.token)


if __name__ == '__main__':
    main()
