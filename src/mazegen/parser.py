#!/usr/bin/env python3
"""Output file generation for maze data."""

from .config import Config
from .utils.mlx_utils import Bit_position


def generate_output(maze: list[list[int]], path: list[str],
                    config: Config) -> bool:
    """
    Generate the output file containing maze details and solution.

    Args:
        maze (list[list[int]]): The maze grid.
        path (list[str]): The solution path as a string of directions.
        config (Config): The configuration object containing output file path.

    Returns:
        bool: True if file generation succeeded, False otherwise.
    """
    try:
        with open(config.OUTPUT_FILE, "w") as f:
            for y in range(config.HEIGHT):
                line = ""
                for x in range(config.WIDTH):
                    n = 0 if (maze[y][x] & Bit_position.NORTH.value) else 1
                    e = 0 if (maze[y][x] & Bit_position.EAST.value) else 1
                    s = 0 if (maze[y][x] & Bit_position.SOUTH.value) else 1
                    w = 0 if (maze[y][x] & Bit_position.WEST.value) else 1
                    hexa = (w << 3) | (s << 2) | (e << 1) | n
                    hex_charset = "0123456789ABCDEF"
                    line += hex_charset[hexa]
                f.write(line+"\n")
            f.write("\n")
            f.write(f"{config.ENTRY[0]},{config.ENTRY[1]}\n")
            f.write(f"{config.EXIT[0]},{config.EXIT[1]}\n")
            f.write("".join(path)+"\n")
        return True
    except Exception:
        return False
