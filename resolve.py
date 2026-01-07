#!/usr/bin/env python3

from config import Config, COLOR_FT, COLOR_STARTING, COLOR_RESET, COLOR_ENDING
import time


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
                print("\033[33m" + full + COLOR_RESET, end='')
        print()


def resolve(maze: list[list[int]], config: Config):
    entry_x, entry_y = config.ENTRY
    exit_x, exit_y = config.EXIT

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # N, S, W, E
    visited = [[False] * config.WIDTH for _ in range(config.HEIGHT)]

    x = entry_x
    y = entry_y
    visited[y][x] = True
    while (not (x == exit_x and y == exit_y)):
        for dir in directions:
            new_x, new_y = x + dir[0], y + dir[1]
            if maze[new_y][new_x] == 0 and not visited[new_y][new_x]:
                x = new_x
                y = new_y
                visited[y][x] = True
                break
            time.sleep(0.5)
            maze[new_y][new_x] = 25
            print_maze(maze, config.EMPTY_CHAR, config.FULL_CHAR)
            maze[new_y][new_x] = 0
    print("found")
