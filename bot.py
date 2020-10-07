import discord
import json


class MyClient(discord.Client):
    restricted_channel = 0
    storage_file = None
    token = None

    def __init__(self):
        super(MyClient, self).__init__()

        try:
            file = open("storage.json", "r+")
            self.storage_file = json.loads(file.read())
        except:
            print("Options file error!")

    async def on_ready(self):
        print('Logged on as', self.user)
        self.restricted_channel = None
        self.token = self.storage_file["token"]

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user and \
                message.channel.id == 609054370415378473:
            return

        if message.content == 'ping':
            await message.channel.send('pong')


def main():
    client = MyClient()
    token = 'NjA4NjY2MDIwNDg3MzY0NjEy.XlJgmw.cHtHW66U_zTP4jFp4rvOx_lvCsc'
    # game = discord.Game("with the API")
    # client.change_presence(status=discord.Status.idle, activity=game)
    client.run(token)


if __name__ == '__main__':
    main()
