import importlib

NAMES = ("codex", "claude")


def load(name):
    if name not in NAMES:
        raise ValueError(f"Unknown hook client: {name}")
    return importlib.import_module(f"clients.{name}")


def from_arguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--client", choices=NAMES, required=True)
    return load(parser.parse_args().client)
