import sys


async def ping(message):
    await message.channel.send("pong")


def example_func(message):
    pass


def get_func(name: str):
    return getattr(sys.modules[__name__], name)