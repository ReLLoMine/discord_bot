import discord
import json
import time


class MyClient(discord.Client):
    main_channel = 0
    storage_file = None
    token = None

    def __init__(self):
        super(MyClient, self).__init__()

        file = open("storage.json", "r+")
        self.storage_file = json.loads(file.read())
        self.token = self.storage_file["token"]
        self.main_channel = self.storage_file["main_channel"]
        self.prefix = self.storage_file["prefix"]
        self.restricted_server = self.storage_file["restricted_server"]

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        content = message.content.split()

        if content[0] == self.prefix and\
                not message.guild.id == self.restricted_server:

            if message.channel.id == self.main_channel:
                if content[1] == 'ping':
                    await message.channel.send('pong')
                    await message.delete()
            else:
                await message.channel.send("Куды пишешь!!!!")
                await message.delete()
        # Security
        elif message.guild.id == self.restricted_server:
            await message.channel.send("Мне сюда низя")


def main():
    client = MyClient()
    # discord.message.Message.guild
    # game = discord.Game("with the API")
    # client.change_presence(status=discord.Status.idle, activity=game)
    client.run(client.token)


if __name__ == '__main__':
    main()
