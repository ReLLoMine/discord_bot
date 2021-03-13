import json
import os
from json import JSONDecodeError

from storage.field import Field
from storage.module_field import ModuleField
from storage.utils import string_xor, create_file_if_not_exist


class Storage(Field):
    def __init__(self, storage=None, filepath: str = "storage.json", key: str = None, save_on_exit=True) -> None:
        """
        :param filepath: Path to file
        :param key: If key is not none file will be encrypted by key
        :param save_on_exit: If true Storage will save all data in case of correct end of program
        """
        super().__init__(self)
        self.__auto_save = save_on_exit
        self.__filepath = filepath
        self.__key = key
        self.load()

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value: str):
        self.__key = value

    @property
    def filepath(self):
        return self.__filepath

    def save(self) -> None:
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
            file.write(string_xor(string, self.key))

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
                data = json.loads(string_xor(file.read(), self.key))
                self.read_class(data)
            except JSONDecodeError:
                pass
        self.split_path()

    def split_path(self):
        self.__filepath = os.path.join(*os.path.split(self.__filepath))

    def __del__(self):
        if self.__auto_save:
            self.save()
