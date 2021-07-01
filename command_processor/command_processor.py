from enum import Enum
from typing import Tuple, List, Any


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

    def _split_input(self, string: str) -> Tuple[str, List[str]]:
        def extract(arr):
            try:
                return arr[0], arr[1:]
            except IndexError:
                return None, None

        return extract([*self.split(string.rstrip(self.prefix))])

    def process_string(self, string: str) -> str:
        string = string.strip()
        if string.startswith(self.prefix):
            if string == "":
                return ""
            cmd, args = self._split_input(string)

            if cmd in self.commands.keys():
                return self.commands[cmd].process(*args)
            else:
                return "Command not found!"

    def process_input(self):
        res = self.process_string(self.input(self.invite))
        if res != "":
            self.output(res)


class BaseCommand:
    """
    mask types: int, any, list-int, list-any, none
    """

    # mask: List[enumerate] = []
    args: List[Any] = []
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
    def process(cls, *args):
        cls._store_args(*args)

        if cls._check_mask():
            return cls.execute()
        else:
            return "Invalid argument(s)"

    @classmethod
    def execute(cls):
        raise NotImplemented
