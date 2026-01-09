#!/usr/bin/env python3

def display_errors(message: str) -> None:
    print(f"\033[31m[ERROR]\033[0m: {message}")


class ArgsException(Exception):
    def __init__(self, *args: str):
        super().__init__(*args)


class ConfigException(Exception):
    def __init__(self, *args: str):
        super().__init__(*args)
