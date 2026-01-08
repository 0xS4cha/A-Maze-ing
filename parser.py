#!/usr/bin/env python3

from config import Config


def generate_output(maze: list[list[int]], path: list[str], config: Config):
    with open(config.OUTPUT_FILE, "w") as f:
        for y in range(1, config.HEIGHT, 2):
            line = ""
            for x in range(1, config.WIDTH, 2):
                n = (maze[y - 1][x] == 0)
                e = (maze[y][x + 1] == 0)
                s = (maze[y + 1][x] == 0)
                w = (maze[y][x - 1] == 0)
                hexa = (w << 3) | (s << 2) | (e << 1) | n
                hex_charset = "0123456789ABCDEF"
                line += hex_charset[hexa]
            f.write(line+"\n")
        f.write("\n")
        f.write(f"{config.ENTRY[0]},{config.ENTRY[1]}\n")
        f.write(f"{config.EXIT[0]},{config.EXIT[1]}\n")
        f.write("".join(path))
