#!/usr/bin/python3
import types
from typing import List

import utils
from server import *
import discord
import my_storage

# Modules
from modules import *


class MyClient(discord.Client):
    intents = discord.Intents.default()
    intents.members = True
    logfile = None

    def __init__(self):
        super(MyClient, self).__init__(intents=self.intents)
        self.storage = my_storage.MyStorage(filepath="storage.json")
        self.servers: List[Server] = {
            server_id: Server(self, self.storage.servers[server_id]) for server_id in self.storage.servers.keys()
        }

        utils.set_exit_handler(self.on_exit)
        self.load_methods()

    def load_methods(self):
        for module_ in modules.sub_modules():
            for name, method in utils.get_functions(module_).items():
                self.__dict__[name] = types.MethodType(method, self)

    @staticmethod
    def reload_modules():
        importlib.reload(modules)

    def run(self):
        super().run(self.storage.token)

    def on_exit(self, sig, func=None):
        self.storage.save()
