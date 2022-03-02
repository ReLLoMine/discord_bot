import bot
import sys
from console_commands import CommandProcessor, Exit, ReloadModules, ChatBuffer


class Program:
    client: bot.MyClient = None
    cp: CommandProcessor = None

    @classmethod
    def main(cls):
        cls.client = bot.MyClient()
        cls.cp = CommandProcessor(
            cls,
            loop=cls.client.loop,
            invite="> ",
            commands={
                "exit": Exit,
                "quit": Exit,
                "reloadmodules": ReloadModules,
                "chatbuffer": ChatBuffer,
            })

        cls.console_run()
        cls.client.run()

    @classmethod
    def console_run(cls):
        future = cls.cp.ensure_future()

    @classmethod
    async def exit(cls):
        cls.cp.stop()
        cls.client.storage.save()
        await cls.client.close()


if __name__ == '__main__':
    Program.main()
