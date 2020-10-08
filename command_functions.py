import comm_functions
import sys
import discord


async def ping(message: discord.Message):
    await message.channel.send("pong")


def example_func(message: discord.Message, args):
    print(args)


async def add_role(message: discord.Message, args):
    await message.guild.create_role()


async def kick_user(message: discord.Message, args):
    if message.author.guild_permissions.kick_members:
        await message.guild.get_member(comm_functions.discord_id(args[0])).kick(
            reason="Loshara")
    else:
        await message.channel.send(f"{message.author.mention} у тебя нет прав "
                                   f"для этой комманды ")


def get_func(name: str):
    return getattr(sys.modules[__name__], name)
