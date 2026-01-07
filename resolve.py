#!/usr/bin/env python3

from config import Config, COLOR_FT, COLOR_STARTING, COLOR_RESET, COLOR_ENDING
import time
import random


def print_maze(maze: list[list[int]], empty, full):
    for line in range(len(maze)):
        for column in range(len(maze[line])):
            if maze[line][column] == 0:
                print(empty, end="")
            elif maze[line][column] == 1:
                print(full, end="")
            elif maze[line][column] == 2:
                print(COLOR_FT + full + COLOR_RESET, end='')
            elif maze[line][column] == 3:
                print(COLOR_STARTING + full + COLOR_RESET,
                      end='')
            elif maze[line][column] == 4:
                print(COLOR_ENDING + full + COLOR_RESET, end='')
            elif maze[line][column] == 25:
                print("\033[32m" + full + COLOR_RESET, end='')
        print()


def resolve(pos: tuple[int, int], direction: int,
            maze: list[list[int]],
            visited: list[list[bool]] | None,
            config: Config) -> bool:
    x, y = pos

    if visited is None:
        visited = [[False] * config.WIDTH for _ in range(config.HEIGHT)]

    if (x, y) == tuple(config.EXIT):
        return True

    visited[y][x] = True

    directions_base = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # N, E, S, W
    directions = [
        directions_base[direction],            # forward
        directions_base[(direction + 3) % 4],  # left
        directions_base[(direction + 1) % 4],  # right
        directions_base[(direction + 2) % 4],  # back
    ]

    for d in directions:
        nx, ny = x + d[0], y + d[1]

        if not (0 <= nx < config.WIDTH and 0 <= ny < config.HEIGHT):
            continue
        if maze[ny][nx] == 1 or maze[ny][nx] == 2 or visited[ny][nx]:
            continue

        if (nx, ny) == tuple(config.EXIT):
            return True

        maze[ny][nx] = 25
        # print_maze(maze, config.EMPTY_CHAR, config.FULL_CHAR)

        if resolve((nx, ny), directions_base.index(d), maze, visited, config):
            return True
        else:
            maze[ny][nx] = 0

    return False
