import json
from json import JSONDecodeError

from storage.field import Field
from storage.module_field import ModuleField
from storage.utils import string_xor, create_file_if_not_exist


class Storage(Field):
    def __init__(self, storage=None, path: str = "./storage.json", key: str = None) -> None:
        """
        :param path: Path to file
        :param key: If key is not none file will be encryption
        """
        super().__init__(self)
        self.__filepath = path
        self.__key = key
        self.load()

    @property
    def key(self):
        return self.__key

    @property
    def filepath(self):
        return self.__filepath

    def save(self) -> None:
        string = json.dumps(self.dict(write_type=True, repr_mod_field=False, save_mod_field=True), indent=2)
        with open(self.filepath, "w", newline='\n') as file:
            file.write(string_xor(string, self.__key))

    def load(self) -> None:
        create_file_if_not_exist(self.filepath, json.dumps(self.dict(write_type=True, repr_mod_field=False,
                                                                     save_mod_field=False), indent=2))
        with open(self.filepath, "r", newline='\n') as file:
            try:
                data = json.loads(string_xor(file.read(), self.__key))
                self.read_class(data)
            except JSONDecodeError:
                pass
        self.save()

    def __del__(self):
        self.save()
