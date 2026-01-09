#!/usr/bin/env python3

import sys


def display_errors(message: str) -> None:
    sys.stderr.write(f"\033[31m[ERROR]\033[0m: {message}\n")


class MazeException(Exception):
    def __init__(self, *args: str):
        super().__init__(*args)


class ArgsException(MazeException):
    def __init__(self, *args: str):
        super().__init__(*args)


class ConfigException(Exception):
    def __init__(self, *args: str):
        super().__init__(*args)
