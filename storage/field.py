import sys
from typing import Dict, Any, List, Union

from storage import get_kwargs


class Field:
    def __init__(self, storage=None):
        self.storage = storage
        self.__setup_fields()

    @property
    def type(self):
        return "Field"

    def __setup_fields(self):
        for name, val in type(self).__dict__.items():
            if not name.startswith("__"):
                if hasattr(val, "storage"):
                    val.storage = self.storage
                self.__dict__[name] = val

    def __get_class(self, name: str) -> type:
        module = __import__(self.__module__)
        if hasattr(module, name):
            return getattr(module, name)
        else:
            class NewClass(Field):
                pass

            NewClass.__name__ = name
            sys.modules[__name__].__dict__[name] = NewClass
            return NewClass

    def __list_dict(self,
                    data: Union[List[Any], Dict[str, Any]],
                    write_type=False,
                    repr_mod_field=True,
                    save_mod_field=False) -> List[Any]:

        result = [Any] * len(data) if isinstance(data, list) else {}
        for key in (range(len(data)) if isinstance(data, list) else data.keys()):
            if isinstance(data[key], list):
                result[key] = self.__list_dict(data[key], write_type, repr_mod_field, save_mod_field)
            elif isinstance(data[key], dict):
                result[key] = self.__list_dict(data[key], write_type, repr_mod_field, save_mod_field)
            elif hasattr(data[key], "type") and data[key].type == "ModuleField":
                result[key] = data[key].dict(write_type, repr_mod_field, save_mod_field) if repr_mod_field else data[
                    key].ref_dict
                if save_mod_field:
                    data[key].save()
            elif hasattr(data[key], 'dict'):
                result[key] = data[key].dict(write_type)
            else:
                result[key] = data[key]
        return result

    def __read_list_dict(self, data: Union[List[Any], Dict[str, Any]]) -> List[Any]:
        result = [Any] * len(data) if isinstance(data, list) else {}
        for key_ in (range(len(data)) if isinstance(data, list) else data.keys()):
            try:
                key = int(key_)
            except ValueError:
                key = key_
            if isinstance(data[key_], list):
                result[key] = self.__read_list_dict(data[key_])
            elif isinstance(data[key_], dict):
                if "__class__" in data[key_]:
                    result[key] = self.__get_class(data[key_]["__class__"])(storage=self.storage)
                    result[key].read_class(data[key_])
                else:
                    result[key] = self.__read_list_dict(data[key_])
            else:
                result[key] = data[key_]
        return result

    def read_class(self, data: Dict[str, Any]) -> None:
        sdict = self.__dict__
        for key in sdict.keys():
            if key in data:
                if isinstance(data[key], list):
                    sdict[key] = self.__read_list_dict(data[key])
                elif isinstance(data[key], dict):
                    if "__class__" in data[key]:
                        sdict[key] = self.__get_class(data[key]["__class__"])(storage=self.storage)
                        sdict[key].read_class(data[key])
                    else:
                        sdict[key] = self.__read_list_dict(data[key])
                else:
                    sdict[key] = data[key]

    def dict(self, write_type=False, repr_mod_field=True, save_mod_field=False) -> Dict[str, Any]:
        kwargs = get_kwargs(write_type=write_type,
                            repr_mod_field=repr_mod_field,
                            save_mod_field=save_mod_field)
        result = {}
        sdict = self.__dict__
        if write_type:
            result["__class__"] = self.__class__.__name__
        for key in sdict.keys():
            if not key.startswith("_") and not key == "storage":
                if isinstance(sdict[key], list):
                    result[key] = self.__list_dict(sdict[key], **kwargs)
                elif isinstance(sdict[key], dict):
                    result[key] = self.__list_dict(sdict[key], **kwargs)
                elif hasattr(sdict[key], "type") and sdict[key].type == "ModuleField":
                    result[key] = sdict[key].dict(**kwargs) if repr_mod_field else self.__dict__[key].ref_dict
                    if save_mod_field:
                        sdict[key].save()
                elif hasattr(sdict[key], 'dict'):
                    result[key] = sdict[key].dict(**kwargs)
                else:
                    if hasattr(sdict[key], '__dict__'):
                        result[key] = sdict[key].__dict__
                    else:
                        result[key] = sdict[key]
        return result
