import os

from pathlib import Path

def string_xor(data: str, key: str) -> str:
    if key in [chr(0), None, ""]:
        return data
    res = ""
    for index in range(len(data)):
        res += chr(ord(data[index]) ^ ord(key[index % len(key)]))
    return res

def create_file_if_not_exist(filepath: str, data: str = "") -> None:
    """
    :param filepath: path to file
    :param data: string which will written in file if it doesn't exist
    """
    if not os.path.exists(filepath):
        file = open(filepath, 'w', newline='\n', encoding="UTF8")
        file.write(data)
        file.close()

def get_kwargs(**kwargs):
    return kwargs
