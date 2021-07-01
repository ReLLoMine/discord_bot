from bot import MyClient
import sys
from console_commands import CommandProcessor, Exit


class Program:
    client: MyClient = None
    cp: CommandProcessor = None

    @classmethod
    def main(cls):
        cls.client = MyClient()
        cls.cp = CommandProcessor(
            cls,
            loop=cls.client.loop,
            invite=">",
            commands={
                "exit": Exit,
                "quit": Exit
            })

        cls.console_run()
        cls.client.run()

    @classmethod
    def console_run(cls):
        future = cls.cp.ensure_future()

    @classmethod
    async def exit(cls):
        cls.cp.stop()
        await cls.client.close()


if __name__ == '__main__':
    Program.main()
