#!/usr/bin/env python3

import random
import time
from utils.mlx_utils import update_cell


def backtrack(x, y, maze, width, height, _config=None, xvar=None):
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        if 0 < nx < width - 1 and 0 < ny < height - 1:
            is_exit = (maze[ny][nx] == 4)
            is_entry = (maze[ny][nx] == 3)
            if maze[ny][nx] == 1 or is_exit or is_entry:
                if not is_exit:
                    maze[ny][nx] = 0
                wx, wy = x + dx // 2, y + dy // 2
                maze[wy][wx] = 0

                if xvar:
                    update_cell(xvar, wx, wy, 0, _config)
                    if not is_exit and not is_entry:
                        update_cell(xvar, nx, ny, 0, _config)
                    if hasattr(_config, 'DELAY') and _config.DELAY > 0:
                        time.sleep(_config.DELAY)
                        xvar.mlx.mlx_do_sync(xvar.mlx_ptr)

                backtrack(nx, ny, maze, width, height, _config, xvar)


def ensure_connectivity(maze, width, height, _config=None, xvar=None):
    for row in range(1, height - 1, 2):
        for col in range(1, width - 1, 2):
            if maze[row][col] == 1:
                neighbors = [(row - 2, col), (row + 2, col), (row, col - 2),
                             (row, col + 2)]
                random.shuffle(neighbors)
                for nx, ny in neighbors:
                    if 0 <= nx < height and 0 <= ny < width and (
                            maze[nx][ny] == 0):
                        maze[row][col] = 0
                        maze[(row + nx) // 2][(col + ny) // 2] = 0
                        backtrack(col, row, maze, width, height, _config, xvar)
                        break


def generate(maze, _config, xvar=None):
    w = _config.WIDTH
    h = _config.HEIGHT

    try:
        entry_x = int(_config.ENTRY[0])
        entry_y = int(_config.ENTRY[1])
        exit_x = int(_config.EXIT[0])
        exit_y = int(_config.EXIT[1])
    except (ValueError, IndexError):
        entry_x, entry_y = 1, 1
        exit_x, exit_y = h - 2, w - 2

    start_x = max(1, min(entry_x, w - 2))
    start_y = max(1, min(entry_y, h - 2))
    if start_x % 2 == 0:
        start_x += 1 if start_x < w - 2 else -1
    if start_y % 2 == 0:
        start_y += 1 if start_y < h - 2 else -1

    maze[entry_y][entry_x] = 3
    maze[exit_y][exit_x] = 4
    update_cell(xvar, entry_x, entry_y, 3, _config)
    update_cell(xvar, exit_x, exit_y, 4, _config)
    backtrack(start_x, start_y, maze, w, h, _config, xvar)

    ensure_connectivity(maze, w, h, _config, xvar)
    return maze
