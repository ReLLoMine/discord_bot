import json
import os
import sys
from json import JSONDecodeError
from pathlib import Path

from storage import utils
from storage.field import Field
from storage.module_field import ModuleField
from storage.utils import string_xor, create_file_if_not_exist


class Storage(Field):
    _base_module = None
    _base_path = None

    def __init__(self, filepath: str = "storage.json", save_on_del=False, crypt_key: str = None) -> None:
        """
        :param filepath: Path to file
        :param crypt_key: If key is not none file will be encrypted by key
        :param save_on_del: If true Storage will save all data in case of correct end of program
        """
        super().__init__(self)
        self._base_module = self.__module__
        self._base_path = Path(sys.modules[self._base_module].__file__).resolve().parent
        self.__save_on_del = save_on_del
        self.__filepath = filepath
        self.__crypt_key = crypt_key
        self.load()

        print("Base directory:", self._base_path)

    @property
    def crypt_key(self):
        return self.__crypt_key

    @crypt_key.setter
    def crypt_key(self, value: str):
        self.__crypt_key = value

    @property
    def filepath(self):
        return os.path.join(self.base_directory, self.__filepath)

    @property
    def related_filepath(self):
        return self.__filepath

    @property
    def base_directory(self):
        return self._base_path

    def save(self) -> None:
        print(f"Storage \"{self.related_filepath}\" saved!")
        string = json.dumps(
            self.dict(
                write_type=True,
                repr_mod_field=False,
                save_mod_field=True
            ),
            indent=2,
            ensure_ascii=False
        )

        with open(self.filepath, "w", newline='\n', encoding="UTF8") as file:
            file.write(string_xor(string, self.crypt_key))

    def load(self) -> None:
        create_file_if_not_exist(
            self.filepath, json.dumps(
                self.dict(
                    write_type=True,
                    repr_mod_field=False,
                    save_mod_field=False
                ),
                indent=2,
                ensure_ascii=False
            )
        )
        with open(self.filepath, "r", newline='\n', encoding="UTF8") as file:
            try:
                data = json.loads(string_xor(file.read(), self.crypt_key))
                self.read_class(data)
            except JSONDecodeError:
                pass
        self.split_path()

    def split_path(self):
        self.__filepath = os.path.join(*os.path.split(self.__filepath))

    def __del__(self):
        if self.__save_on_del:
            self.save()

    def __iter__(self):
        for name, val in self.dict().items():
            yield name, val

    def __getitem__(self, item):
        return self.dict()[item]

    def keys(self):
        for name in self.dict().keys():
            yield name
