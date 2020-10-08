import discord
import json
import time
import sys
import command_functions


def str_to_class(string):
    return getattr(sys.modules[__name__], string)


class Command:

    def __init__(self, keyname=None, mask=None, function=None, cmd_dict=None):
        if cmd_dict is not None:
            self.read_from_dict(cmd_dict)

        if keyname is not None:
            self.keyname = keyname
        if mask is not None:
            self.mask = mask
        if function is not None:
            self.function = function

    def check_content(self, content):
        raise NotImplementedError

    def read_from_dict(self, command):
        self.keyname = command["keyname"]
        self.mask = command["mask"]
        self.function = getattr(command_functions, command["function"])


class Commands:

    def __init__(self, commands=None):
        self.commands = {}

        if commands is None:
            commands = {}
        else:
            self.read_from_dict(commands)

    def read_from_dict(self, commands):
        for cmd in commands:
            self.commands[cmd["keyname"]] = Command(cmd_dict=cmd)

    def add_command(self, command):
        self.commands[command.keyname] = command


class Server:

    def __init__(self, server_id=None,
                 prefix=None,
                 commands=None,
                 server_dict=None,
                 is_debug=False):

        if server_dict is not None:
            self.read_from_dict(server_dict)

        if server_id is not None:
            self.server_id = str(server_id)
        if prefix is not None:
            self.prefix = prefix
        if commands is not None:
            self.commands = Commands(commands)

        self.is_debug = is_debug

    def read_from_dict(self, server):
        self.server_id = server["server_id"]
        self.prefix = server["prefix"]
        self.commands = Commands(commands=server["commands"])


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
            self.servers[server["server_id"]] = Server(server)

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        content = message.content.split()


'''
        if content[0] == self.prefix and \
                not message.guild.id == self.restricted_server:

            if message.channel.id == self.main_channel:
                if content[1] == 'ping':
                    await message.channel.send('pong')
            else:
                await message.channel.send("Куды пишешь!!!!")
                await message.delete()
        # Security
        elif message.guild.id == self.restricted_server:
            await message.channel.send("Мне сюда низя")
'''


def main():
    client = MyClient()
    # discord.message.Message.guild
    # game = discord.Game("with the API")
    # client.change_presence(status=discord.Status.idle, activity=game)
    client.run(client.token)


if __name__ == '__main__':
    main()
