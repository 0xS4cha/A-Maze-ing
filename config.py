#!/usr/bin/env python3

import exception
import sys

sys.setrecursionlimit(2000)

COLOR_STARTING = "\033[35m"
COLOR_ENDING = "\033[31m"
COLOR_FT = "\033[0;36m"
COLOR_RESET = "\033[0m"


class Config:
    @staticmethod
    def get_error_line_format(i: int, config_path: str) -> str:
        return f"\tFile \"{config_path}\", line {i}\n"

    def __init__(self, config_path: str) -> None:
        self.WIDTH = 0
        self.HEIGHT = 0
        self.ENTRY = [0, 0]
        self.EXIT = [0, 0]
        self.OUTPUT_FILE = ""
        self.PERFECT = False
        self.EMPTY_CHAR = ' '
        self.FULL_CHAR = '█'
        self.DELAY = 0
        self.COLORS = {
            0: 0xFF1E1E2E,  # empty -> Dark Blue/Black background (Base)
            1: 0xFF45475A,  # wall -> Soft Grey/Blue (Surface)
            2: 0xFFF9E2AF,  # ft symbol -> Gold/Yellow (Accent principal)
            3: 0xFFA6E3A1,  # start -> Soft Green
            4: 0xFFF38BA8,  # end -> Soft Red
        }
        with open(config_path, "r") as f:
            for i, line in enumerate(f.readlines()):
                if line.strip().startswith("#"):
                    continue  # skip comments
                separator_idx = line.find("=")
                if separator_idx == -1:
                    raise exception.ConfigException(f"Entry is not a \
definition: {line}.\n{self.get_error_line_format(i+1, config_path)}")
                left_arg = line[:separator_idx].strip()
                right_arg = line[separator_idx + 1:].strip()
                try:
                    if left_arg == "WIDTH" and int(right_arg) > 0:
                        self.WIDTH = int(right_arg)
                    elif left_arg == "HEIGHT" and int(right_arg) > 0:
                        self.HEIGHT = int(right_arg)
                    elif left_arg == "DELAY":
                        self.DELAY = float(right_arg)
                    elif (left_arg == "ENTRY" or
                          left_arg == "EXIT") and right_arg.find(",") != -1:
                        entry = right_arg.split(",")
                        if (len(entry) != 2):
                            raise
                        if left_arg == "ENTRY":
                            self.ENTRY[0] = int(entry[0].strip()) + 1
                            self.ENTRY[1] = int(entry[1].strip()) + 1
                        else:
                            self.EXIT[0] = int(entry[0].strip()) + 1
                            self.EXIT[1] = int(entry[1].strip()) + 1
                    elif left_arg == "OUTPUT_FILE":
                        self.OUTPUT_FILE = right_arg
                    elif left_arg == "PERFECT":
                        self.PERFECT = bool(right_arg)
                    elif left_arg == "ALGORITHMS":
                        self.ALGORITHMS = int(right_arg)
                    elif left_arg == "ANIMATION":
                        self.ANIMATION = bool(right_arg)
                    elif left_arg == "GRAPHIC":
                        self.GRAPHIC = int(right_arg)
                    else:
                        raise ValueError(f"Unknown entry: {line}.")
                except ValueError as e:
                    raise exception.ConfigException(f"Invalid config entry: \
{e.args[0]}.\n{self.get_error_line_format(i+1, config_path)}")
