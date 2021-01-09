from typing import List

import storage


class CommandField(storage.Field):
    def __init__(self):
        self.keyname = "example"
        self.function = "example_func"
        self.description = "example description"
        self.is_blacklisted = False
        self.channel_whitelist = []
        self.channel_blacklist = []


class ServerField(storage.Field):
    def __init__(self):
        self.server_id = 0
        self.prefix = ">>"
        self.origin_channel_category = 0
        self.target_create_channel_category = 0
        self.created_channels = []
        self.commands: List[CommandField] = []


class MyStorage(storage.Storage):
    def __init__(self, **args):
        self.token = "token"
        self.owner_id = 401090419448086528
        self.debug_server = 619267511589797889
        self.default_commands: List[CommandField] = []
        self.servers: List[ServerField] = []
        super().__init__(**args)
