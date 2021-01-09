import json
import os
import sys
from json import JSONDecodeError
from typing import Dict, Any, List


def create_file_if_not_exist(filepath: str, data: str = "") -> None:
    """
    :param filepath: path to file
    :param data: string which will written in file if it doesn't exist
    """
    if not os.path.exists(filepath):
        file = open(filepath, 'w')
        file.write(data)
        file.close()


class Field:
    def __get_class(self, name: str) -> type:
        module = __import__(self.__module__)
        if hasattr(module, name):
            return getattr(module, name)
        else:
            class new_class(Field):
                def read_class(self, json_dict: Dict[str, Any]) -> None:
                    for key in json_dict.keys():
                        if isinstance(json_dict[key], list):
                            self.__dict__[key] = self.__read_list(json_dict[key])
                        elif isinstance(json_dict[key], dict) and "__class__" in json_dict[key]:
                            self.__dict__[key] = self.__get_class(json_dict[key]["__class__"])()
                            self.__dict__[key].read_class(json_dict[key])
                        else:
                            self.__dict__[key] = json_dict[key]

            new_class.__name__ = name
            sys.modules[__name__].__dict__[name] = new_class
            return new_class

    def dict(self, write_type: bool = False) -> Dict[str, Any]:
        result = {}
        if write_type:
            result["__class__"] = self.__class__.__name__
        for key in self.__dict__.keys():
            if not key.startswith("_"):
                if isinstance(self.__dict__[key], list):
                    result[key] = self.__list(self.__dict__[key], write_type)
                elif isinstance(self.__dict__[key], dict):
                    result[key] = self.__dict(self.__dict__[key], write_type)
                elif hasattr(self.__dict__[key], 'dict'):
                    result[key] = self.__dict__[key].dict(write_type)
                else:
                    if hasattr(self.__dict__[key], '__dict__'):
                        result[key] = self.__dict__[key].__dict__
                    else:
                        result[key] = self.__dict__[key]
        return result

    def __list(self, data: List[Any], write_type: bool = False) -> List[Any]:
        result = [Any] * len(data)
        for index in range(len(data)):
            if isinstance(data[index], list):
                result[index] = self.__list(data[index], write_type)
            elif isinstance(data[index], dict):
                result[index] = self.__dict(data[index], write_type)
            elif hasattr(data[index], 'dict'):
                result[index] = data[index].dict(write_type)
            else:
                result[index] = data[index]
        return result

    def __dict(self, data: Dict[str, Any], write_type: bool = False) -> Dict[str, Any]:
        result = {}
        for key in data.keys():
            if isinstance(data[key], list):
                result[key] = self.__list(data[key], write_type)
            elif isinstance(data[key], dict):
                result[key] = self.__dict(data[key], write_type)
            elif hasattr(data[key], 'dict'):
                result[key] = data[key].dict(write_type)
            else:
                result[key] = data[key]
        return result

    def __read_list(self, data: List[Any]) -> List[Any]:
        result = [Any] * len(data)
        for index in range(len(data)):
            if isinstance(data[index], list):
                result[index] = self.__read_list(data[index])
            elif isinstance(data[index], dict):
                if "__class__" in data[index]:
                    result[index] = self.__get_class(data[index]["__class__"])()
                    result[index].read_class(data[index])
                else:
                    result[index] = self.__read_dict(data[index])
            else:
                result[index] = data[index]
        return result

    def __read_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {}
        for key in data.keys():
            if isinstance(data[key], list):
                result[key] = self.__read_list(data[key])
            elif isinstance(data[key], dict):
                if "__class__" in data[key]:
                    result[key] = self.__get_class(data[key]["__class__"])()
                    result[key].read_class(data[key])
                else:
                    result[key] = self.__read_dict(data[key])
            else:
                result[key] = data[key]
        return result

    def read_class(self, json_dict: Dict[str, Any]) -> None:
        for key in self.__dict__.keys():
            if key in json_dict:
                if isinstance(json_dict[key], list):
                    self.__dict__[key] = self.__read_list(json_dict[key])
                elif isinstance(json_dict[key], dict):
                    if "__class__" in json_dict[key]:
                        self.__dict__[key] = self.__get_class(json_dict[key]["__class__"])()
                        self.__dict__[key].read_class(json_dict[key])
                    else:
                        self.__dict__[key] = self.__read_dict(json_dict[key])
                else:
                    self.__dict__[key] = json_dict[key]


class Storage(Field):
    def __init__(self, path: str = "./storage.json") -> None:
        super().__init__()
        self.__filepath = path
        self.load()

    def save(self) -> None:
        string = json.dumps(self.dict(write_type=True), indent=2)
        with open(self.__filepath, "w") as file:
            file.write(string)

    def load(self) -> None:
        create_file_if_not_exist(self.__filepath, json.dumps(self.dict(write_type=True), indent=2))
        with open(self.__filepath, "r") as file:
            try:
                json_dict = json.load(file)
                self.read_class(json_dict)
            except JSONDecodeError:
                pass
        self.save()

    def __del__(self):
        self.save()
