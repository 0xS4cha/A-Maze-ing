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
        if maze[ny][nx] == 1 or visited[ny][nx]:
            continue

        if (nx, ny) == tuple(config.EXIT):
            return True

        maze[ny][nx] = 25
        print_maze(maze, config.EMPTY_CHAR, config.FULL_CHAR)
        time.sleep(0.05)

        if resolve((nx, ny), directions_base.index(d), maze, visited, config):
            return True
        else:
            maze[ny][nx] = 0

    return False


#def resolve(maze: list[list[int]], config: Config):
#    entry_x, entry_y = config.ENTRY
#    exit_x, exit_y = config.EXIT

#    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # N, S, W, E
#    visited = [[False] * config.WIDTH for _ in range(config.HEIGHT)]

#    x = entry_x
#    y = entry_y
#    visited[y][x] = True
#    while (not (x == exit_x and y == exit_y)):
#        found = False
#        random.shuffle(directions)
#        for dir in directions:
#            new_x, new_y = x + dir[0], y + dir[1]
#            if maze[new_y][new_x] == 0 and not visited[new_y][new_x]:
#                x = new_x
#                y = new_y
#                visited[y][x] = True
#                time.sleep(0.2)
#                maze[new_y][new_x] = 25
#                print_maze(maze, config.EMPTY_CHAR, config.FULL_CHAR)
#                maze[new_y][new_x] = 0
#                found = True
#                break
        #if not found:
            
