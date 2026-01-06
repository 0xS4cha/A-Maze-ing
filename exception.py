#!/usr/bin/env python3


def display_errors(message: str) -> None:
    print(f"[ERROR]: {message}")


class ArgsException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ConfigException(Exception):
    def __init__(self, *args):
        super().__init__(*args)