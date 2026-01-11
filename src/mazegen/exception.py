#!/usr/bin/env python3
"""Custom exceptions for the maze generator."""

import sys


def display_errors(message: str) -> None:
    """
    Print error messages to standard error in red.

    Args:
        message (str): The error message to display.
    """
    sys.stderr.write(f"\033[31m[ERROR]\033[0m: {message}\n")


class MazeException(Exception):
    """
    Base exception class for maze generation errors.

    Args:
        *args (str): Variable length argument list.
    """

    def __init__(self, *args: str):
        super().__init__(*args)


class ArgsException(MazeException):
    """
    Exception raised for invalid command-line arguments.

    Args:
        *args (str): Variable length argument list.
    """

    def __init__(self, *args: str):
        super().__init__(*args)


class ConfigException(Exception):
    """
    Exception raised for configuration file errors.

    Args:
        *args (str): Variable length argument list.
    """

    def __init__(self, *args: str):
        super().__init__(*args)
