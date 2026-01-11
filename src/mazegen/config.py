#!/usr/bin/env python3
"""Configuration handling for the maze generator."""

from . import exception
import sys

sys.setrecursionlimit(100000)

COLOR_STARTING = "\033[35m"
COLOR_ENDING = "\033[31m"
COLOR_FT = "\033[0;36m"
COLOR_RESET = "\033[0m"


class Config:
    """
    Configuration class for parsing and storing settings.

    Attributes:
        WIDTH (int): Maze width.
        HEIGHT (int): Maze height.
        ENTRY (list[int]): Entry coordinates [x, y].
        EXIT (list[int]): Exit coordinates [x, y].
        OUTPUT_FILE (str): Path to output file.
        PERFECT (int): Algorithm choice (False=Eller/Prim, True=stacking).
        ANIMATION (int): Animation check.
        COLORS (list[dict]): List of color palettes.
    """

    @staticmethod
    def get_error_line_format(i: int, config_path: str) -> str:
        """
        Format error messages for configuration parsing.

        Args:
            i (int): Line number.
            config_path (str): Path to config file.

        Returns:
            str: Formatted error string.
        """
        return f"\tFile \"{config_path}\", line {i}\n"

    def __init__(self, config_path: str) -> None:
        """
        Initialize configuration from a file.

        Args:
            config_path (str): Path to the configuration file.

        Raises:
            exception.ConfigException: If configuration is invalid.
        """
        self.WIDTH = 0
        self.HEIGHT = 0
        self.ENTRY = [0, 0]
        self.EXIT = [0, 0]
        self.OUTPUT_FILE = ""
        self.PERFECT = False
        self.ANIMATION = 1
        self.DELAY = 0.001
        self.SEED = "0"
        self.COLORS = [
            {
                0: 0xFF1E1E2E,  # empty -> Dark Blue/Black background (Base)
                1: 0xFF45475A,  # wall -> Soft Grey/Blue (Surface)
                2: 0xFFF9E2AF,  # ft symbol -> Gold/Yellow (Accent principal)
                3: 0xFFA6E3A1,  # start -> Soft Green
                4: 0xFFF38BA8,  # end -> Soft Red
                5: 0xFFFFFFFF   # path -> White
            },
            {
                0: 0xFFF5F5F7,  # empty -> White
                1: 0xFFD1D1D6,  # wall -> Gray
                2: 0xFFFF9500,  # ft symbol -> Orange
                3: 0xFF34C759,  # start -> Green
                4: 0xFFFF3B30,  # end -> Red
                5: 0xFF1C1C1E   # path -> black
            },
            {
                0: 0xFF0F380F,  # empty -> Dark Green
                1: 0xFF306230,  # wall -> Green
                2: 0xFF8BAC0F,  # ft symbol -> Accent Green
                3: 0xFFFFFFFF,  # start -> White
                4: 0xFF000000,  # end -> Black
                5: 0xFF9BBC0F   # path -> Green
            },
            {
                0: 0xFF001F3F,  # empty -> Dark Blue
                1: 0xFF3A6D8C,  # wall -> Steel Blue
                2: 0xFFFF851B,  # ft symbol -> Orange
                3: 0xFF2ECC40,  # start -> Green
                4: 0xFFFF4136,  # end -> Red Brick
                5: 0xFF7FDBFF   # path -> Blue
            },
            {
                0: 0xFF240046,  # empty -> Dark Purple
                1: 0xFF5A189A,  # wall -> Purple
                2: 0xFFFF9E00,  # ft symbol -> Orange
                3: 0xFF00B4D8,  # start -> Blue
                4: 0xFFF72585,  # end -> Magenta
                5: 0xFFE0AAFF   # path -> Lavander
            }
        ]
        try:
            with open(config_path, "r") as f:
                for i, line in enumerate(f.readlines()):
                    if line.strip().startswith("#") or len(line.strip()) == 0:
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
                              left_arg == "EXIT") and \
                                right_arg.find(",") != -1:
                            entry = right_arg.split(",")
                            if (len(entry) != 2):
                                raise
                            if left_arg == "ENTRY":
                                self.ENTRY[0] = int(entry[0].strip())
                                self.ENTRY[1] = int(entry[1].strip())
                            else:
                                self.EXIT[0] = int(entry[0].strip())
                                self.EXIT[1] = int(entry[1].strip())
                        elif left_arg == "OUTPUT_FILE":
                            self.OUTPUT_FILE = right_arg
                        elif left_arg == "PERFECT":
                            if right_arg == "True":
                                self.PERFECT = True
                            else:
                                self.PERFECT = False
                        elif left_arg == "ANIMATION":
                            self.ANIMATION = int(right_arg)
                        elif left_arg == "SEED":
                            self.SEED = right_arg
                        else:
                            raise ValueError(f"Unknown entry: '{line}'.")
                    except ValueError as e:
                        raise exception.ConfigException(f"Invalid config \
entry:  {e.args[0]}.\n{self.get_error_line_format(i+1, config_path)}")
        except (FileExistsError, FileNotFoundError, PermissionError):
            raise exception.ConfigException(f"File '{config_path}' \
is not accessible")
