import importlib
import modules.voice
import modules.on_start
import modules.runtime

__exceptions = {"importlib"}
__modulenames = set(globals()) ^ __exceptions
__allmodules = set([globals()[name] for name in __modulenames if not name.startswith("__")])

for module in __allmodules:
    importlib.reload(module)

def sub_modules():
    return __allmodules
