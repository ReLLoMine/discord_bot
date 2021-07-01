import sys

from command_processor.command_processor import *
import asyncio

class Mask(Enum):
    int = 0
    any = 1
    list = 2
    none = 3


class AIOBaseCommandProcessor(BaseCommandProcessor):

    def __init__(self, loop=None, **kwargs):
        super().__init__(**kwargs)

        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.done = False

        def stop_loop_on_completion(f):
            self.loop.stop()

        self.stop_loop_on_completion = stop_loop_on_completion

    def stop(self):
        self.done = True

    async def process_string(self, string: str) -> str:
        string = string.strip()
        if string.startswith(self.prefix):
            if string == "":
                return ""
            cmd, args = self._split_input(string)

            if cmd in self.commands.keys():
                return await self.commands[cmd].process(*args)
            else:
                return "Command not found!"

    async def process_input(self):
        res = await self.process_string(await self.aio_input())
        if res != "":
            self.output(res)

    def _cancel_tasks(self):
        task_retriever = asyncio.all_tasks

        tasks = {t for t in task_retriever(loop=self.loop) if not t.done()}

        if not tasks:
            return

        print(f'Cleaning up after {len(tasks)} tasks.')
        for task in tasks:
            task.cancel()

        self.loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        print('All tasks finished cancelling.')

        for task in tasks:
            if task.cancelled():
                continue
            if task.exception() is not None:
                self.loop.call_exception_handler({
                    'message': 'Unhandled exception during Client.run shutdown.',
                    'exception': task.exception(),
                    'task': task
                })

    def shutdown(self):

        try:
            self._cancel_tasks()
            if sys.version_info >= (3, 6):
                self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        finally:
            print('Closing the event loop.')
            self.loop.close()

    async def aio_input(self):
        return await self.loop.run_in_executor(None, self.input, self.invite)

    def ensure_future(self):
        async def runner():
            while not self.done:
                await self.process_input()

        future = asyncio.ensure_future(runner(), loop=self.loop)

        return future

    def run(self):
        self.done = False

        future = self.ensure_future()
        future.add_done_callback(self.stop_loop_on_completion)

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            print('Received signal to terminate bot and event loop.')
        finally:
            future.remove_done_callback(self.stop_loop_on_completion)
            print('Cleaning up tasks.')
            self.shutdown()


class AIOBaseCommand(BaseCommand):
    """
    mask types: int, any, list-int, list-any, none
    """

    # mask: List[enumerate] = []
    cmdproc: AIOBaseCommandProcessor = None

    @classmethod
    async def process(cls, *args):
        cls._store_args(*args)

        if cls._check_mask():
            return await cls.execute()
        else:
            return "Invalid argument(s)"

    @classmethod
    async def execute(cls):
        raise NotImplemented
