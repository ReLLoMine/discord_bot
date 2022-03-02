import discord


from my_storage import ServerField


async def on_message_edit(self, before, after):
    pass

async def on_message_delete(self, message):
    pass

async def on_typing(self, channel, user, when):
    pass

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
        elif message.content == "RELOAD-7311097":
            self.reload_modules()
            await message.channel.send("Modules reloaded successfully!")
        else:
            await message.channel.send(message.content)

    elif message.channel.type is discord.ChannelType.text:
        self.servers[message.guild.id].cp.push_message(message)
        await self.servers[message.guild.id].cp.process_input()

async def on_guild_join(self, guild: discord.Guild):
    server = ServerField(storage=self.storage)
    server.server_id = guild.id
    self.storage.servers[guild.id] = server
    self.servers[guild.id] = type(self)(self, server)
    self.storage.save()
