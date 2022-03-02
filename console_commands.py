from command_processor.aio_command_processor import AIOBaseCommand, AIOBaseCommandProcessor


class CommandProcessor(AIOBaseCommandProcessor):

    def __init__(self, program, **kwargs):
        self.program = program
        super().__init__(**kwargs)

class Exit(AIOBaseCommand):

    @classmethod
    async def execute(cls):
        await cls.cmdproc.program.exit()
        return "Goodbye!"

class ReloadModules(AIOBaseCommand):

    @classmethod
    async def execute(cls):
        cls.cmdproc.program.client.reload_modules()
        return "Modules reloaded successfully"

class ChatBuffer(AIOBaseCommand):
    @classmethod
    async def execute(cls):
        if cls.get_arg(0) is not IndexError:
            return cls.cmdproc.program.client.servers[cls.get_arg(0)].cp.chat_buffer
        else:
            return "IndexError"
