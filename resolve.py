#!/usr/bin/env python3

from config import Config, COLOR_FT, COLOR_STARTING, COLOR_RESET, COLOR_ENDING
import time
import random
from collections import deque


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
            config: Config) -> list[str] | bool:
    queue = deque([pos])
    visited_set = {pos}
    came_from = {pos: None}
    end_pos = tuple(config.EXIT)

    final_node = None

    while queue:
        current = queue.popleft()

        if current == end_pos:
            final_node = current
            break

        x, y = current
        # Directions: N, E, S, W
        movements = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        for dx, dy in movements:
            nx, ny = x + dx, y + dy

            if not (0 <= nx < config.WIDTH and 0 <= ny < config.HEIGHT):
                continue

            if maze[ny][nx] == 1 or maze[ny][nx] == 2:
                continue

            if (nx, ny) not in visited_set:
                visited_set.add((nx, ny))
                came_from[(nx, ny)] = current
                queue.append((nx, ny))

    if final_node:
        # Reconstruct path
        path = []
        curr = final_node
        while curr != pos:
            parent = came_from[curr]
            dx, dy = curr[0] - parent[0], curr[1] - parent[1]

            if dx == 0 and dy == -1:
                d = "N"
            elif dx == 1 and dy == 0:
                d = "E"
            elif dx == 0 and dy == 1:
                d = "S"
            elif dx == -1 and dy == 0:
                d = "W"
            path.append(d)

            if curr != end_pos:
                maze[curr[1]][curr[0]] = 25
            curr = parent
        path.reverse()
        return path
    return False

