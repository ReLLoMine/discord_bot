import discord

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
