import typing
import asyncio
from enum import Enum


def is_async(func):
    return asyncio.iscoroutinefunction(func)

class Mask(Enum):
    int = 0
    any = 1
    list = 2
    none = 3

class BaseCommandProcessor:

    def __init__(self, prefix="", invite="", commands=None, _input=input, _output=print):
        self.prefix = prefix
        self.invite = invite
        self.commands = {} if commands is None else commands
        self.input = _input
        self.output = _output
        self._set_cp()

    def _set_cp(self):
        for cmd in self.commands.values():
            cmd.cmdproc = self

    @staticmethod
    def split(string: str):
        tmp_string = ""
        is_screen = False

        for char in string:
            if char == '"':
                is_screen = not is_screen
            elif char != " " or is_screen:
                tmp_string += char
            else:
                if tmp_string != "":
                    yield tmp_string
                tmp_string = ""

        if tmp_string != "":
            yield tmp_string

    def _split_input(self, string: str) -> typing.Tuple[str, typing.List[str]]:

        def extract(arr):
            try:
                return arr[0], arr[1:]
            except IndexError:
                return None, None

        return extract([*self.split(string.rstrip(self.prefix))])

    async def process_string(self, string: str) -> str:
        string = string.strip()
        if string.startswith(self.prefix):
            if string == "":
                return None
            cmd, args = self._split_input(string.lstrip(self.prefix))

            if cmd in self.commands.keys():
                return await self.commands[cmd].process(*args)
            else:
                return "Command not found!"
        return None

    async def process_input(self, _input=None):
        if _input is None:
            if is_async(self.input):
                string = await self.input(self.invite)
            else:
                string = self.input(self.invite)

            res = await self.process_string(string)
        else:
            res = await self.process_string(_input)

        if res is not None:
            if is_async(self.output):
                await self.output(res)
            else:
                self.output(res)

class BaseCommand:
    """
    mask types: int, any, list-int, list-any, none
    """

    # mask: List[enumerate] = []
    args: typing.List[typing.Any] = []
    cmdproc: BaseCommandProcessor = None

    @classmethod
    def _try_convert(cls):
        for index in range(len(cls.args)):
            try:
                cls.args[index] = int(cls.args[index])
            except ValueError:
                try:
                    cls.args[index] = float(cls.args[index])
                except ValueError:
                    pass

    @classmethod
    def _check_mask(cls):
        # if len(cls.mask) > len(cls.args):
        #     return False

        cls._try_convert()

        # for index in range(len(cls.mask)):
        #     if cls.mask[index] is Mask.int:
        #         if not isinstance(cls.args[index], int):
        #             return False
        #     # elif cls.mask[index] == "list" and index != len(cls.mask) - 1:
        #     #     return False
        #     elif cls.mask[index] is Mask.any:
        #         pass

        return True

    @classmethod
    def _store_args(cls, *args):
        cls.args = list(args)

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

    @classmethod
    def get_arg(cls, idx=0):
        if idx < len(cls.args):
            return cls.args[0]
        else:
            return IndexError
