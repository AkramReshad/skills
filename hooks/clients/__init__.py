import importlib

NAMES = ("codex", "claude")


def load(name):
    if name not in NAMES:
        raise ValueError(f"Unknown hook client: {name}")
    return importlib.import_module(f"clients.{name}")


def from_arguments(arguments):
    if len(arguments) != 2 or arguments[0] != "--client":
        raise ValueError(f"Expected --client {{{','.join(NAMES)}}}, got: {' '.join(arguments) or 'no arguments'}")
    return load(arguments[1])
