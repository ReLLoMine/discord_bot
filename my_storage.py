from typing import List, Dict

import storage


class CommandField(storage.Field):
    def __init__(self, **args):
        super().__init__(**args)
        self.keyname = "example"
        self.function = "example_func"
        self.description = "example description"
        self.is_blacklisted = False
        self.channel_whitelist = []
        self.channel_blacklist = []


class ServerField(storage.ModuleField):
    def __init__(self, **args):
        super().__init__(**args)
        self.server_id = 0
        self.prefix = ">>"
        self.origin_channel_category = 0
        self.target_create_channel_category = 0
        self.created_channels = []
        #self.commands: List[CommandField] = []

        self._path_dir = "servers"
        self._extension = "json"
        self._keyname = "server_id"


class MyStorage(storage.Storage):
    def __init__(self, **args):
        self.token = "Nzk3NDY4NjkwNjUxODA3ODA2.X_m6mA.MgFn0NDYfkDx0b8zTEnq-IR07o8"
        self.owner_id = 401090419448086528
        self.debug_server = 619267511589797889
        #self.default_commands: List[CommandField] = []
        self.servers: Dict[int, ServerField] = {}
        super().__init__(**args)
