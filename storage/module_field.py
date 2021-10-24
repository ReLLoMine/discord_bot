import json
import os
from json.decoder import JSONDecodeError
from typing import Any, Dict

from .utils import string_xor, create_file_if_not_exist
from .field import Field


class ModuleField(Field):
    _path_dir: str = ""
    _extension: str = ""
    _keyname: str = None

    @property
    def type(self):
        return "ModuleField"

    def filepath(self, keyname: str = None):
        return os.path.join(
            self.storage.base_directory,
            self._path_dir,
            (self.keyname if keyname is None else keyname) + self.extension
        )

    def related_filepath(self, keyname: str = None):
        return os.path.join(
            self._path_dir,
            (self.keyname if keyname is None else keyname) + self.extension
        )

    @property
    def ref_dict(self):
        return {
            "__class__": self.__class__.__name__,
            "path": self.related_filepath()
        }

    @property
    def keyname(self):
        if self._keyname not in self.__dict__.keys():
            raise Exception("_keyname not defined")
        return str(getattr(self, self._keyname))

    @property
    def extension(self):
        return "." + self._extension if self._extension != "" else ""

    def save(self):
        string = json.dumps(
            self.dict(
                write_type=True,
                repr_mod_field=False,
                save_mod_field=True
            ),
            indent=2,
            ensure_ascii=False
        )
        with open(self.filepath(), "w", newline='\n', encoding="UTF8") as file:
            file.write(string_xor(string, self.storage.crypt_key))

    def load(self, keyname: str = None):
        create_file_if_not_exist(
            self.filepath(), json.dumps(
                self.dict(
                    write_type=True,
                    repr_mod_field=False,
                    save_mod_field=False
                ),
                indent=2,
                ensure_ascii=False
            )
        )

        with open(self.filepath(keyname), "r", newline='\n', encoding="UTF8") as file:
            try:
                json_dict = json.loads(string_xor(file.read(), self.storage.crypt_key))
                super().read_class(json_dict)
            except JSONDecodeError:
                pass
        self.save()

    def split_path(self):
        self._path_dir = os.path.join(*os.path.split(self._path_dir))

    def read_class(self, data: Dict[str, Any]) -> None:
        path = list(os.path.split(data["path"].replace("\\", "/")))
        self._path_dir = os.path.join(*path[:-1])
        self._extension = path[-1].split(".")[-1] if path[-1].find(".") != -1 else ""
        self.load(path[-1].rstrip(self.extension))
