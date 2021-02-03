import json
import os
from json.decoder import JSONDecodeError
from typing import Any, Dict

from .utils import string_xor, create_file_if_not_exist
from .field import Field


class ModuleField(Field):
    def __init__(self, **args):
        super().__init__(**args)
        self._path_dir: str = ""
        self._keyname: str = None
        self._extension: str = None

    @property
    def type(self):
        return "ModuleField"

    def filepath(self, keyname: str = None):
        if self.keyname in [None, ""]:
            raise Exception("self.__keyname is not defined!")
        return os.path.join(self._path_dir, (self.keyname if keyname is None else keyname) + self.extension)

    @property
    def ref_dict(self):
        return {
            "__class__": self.__class__.__name__,
            "path": self.filepath()
        }

    @property
    def keyname(self):
        return str(getattr(self, self._keyname))

    @property
    def extension(self):
        return "." + self._extension if self._extension != "" else ""

    def save(self):
        string = json.dumps(self.dict(write_type=True), indent=2)
        with open(self.filepath(), "w", newline='\n') as file:
            file.write(string_xor(string, self._storage.key))

    def load(self, keyname: str = None):
        create_file_if_not_exist(self.filepath(keyname), json.dumps(self.dict(write_type=True), indent=2))

        with open(self.filepath(keyname), "r", newline='\n') as file:
            try:
                json_dict = json.loads(string_xor(file.read(), self._storage.key))
                super().read_class(json_dict)
            except JSONDecodeError:
                pass
        self.save()

    def read_class(self, data: Dict[str, Any]) -> None:
        path = list(os.path.split(data["path"]))
        self._path_dir = os.path.join(*path[:-1])
        self._extension = path[-1].split(".")[-1] if path[-1].find(".") != -1 else ""
        self.load(path[-1].rstrip(self.extension))
