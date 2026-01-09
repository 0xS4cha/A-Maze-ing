#!/usr/bin/env python3

from .config import Config


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
            for y in range(1, config.HEIGHT, 2):
                line = ""
                for x in range(1, config.WIDTH, 2):
                    n = (maze[y - 1][x] == 1)
                    e = (maze[y][x + 1] == 1)
                    s = (maze[y + 1][x] == 1)
                    w = (maze[y][x - 1] == 1)
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
