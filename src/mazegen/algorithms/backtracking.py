#!/usr/bin/env python3
"""Recursive backtracking algorithm for maze generation."""

import random
import time
from ..utils.mlx_utils import XVar, update_cell
from ..config import Config


def backtrack(x: int, y: int, maze: list[list[int]], width: int, height: int,
              _config: Config, xvar: XVar) -> None:
    """
    Generate a maze using the recursive backtracking algorithm.

    Args:
        x (int): Current x-coordinate.
        y (int): Current y-coordinate.
        maze (list[list[int]]): 2D list representing the maze grid.
        width (int): Width of the maze.
        height (int): Height of the maze.
        _config (Config): Configuration object.
        xvar (XVar): Graphics context for animation.
    """
    if maze[y][x] == 4:
        return

    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        if 0 < nx < width - 1 and 0 < ny < height - 1:
            is_exit = (maze[ny][nx] == 4)
            is_entry = (maze[ny][nx] == 3)

            if is_exit:
                exit_connected = False
                for ex_dx, ex_dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    ex_nx, ex_ny = nx + ex_dx, ny + ex_dy
                    if 0 <= ex_nx < width and 0 <= ex_ny < height:
                        if maze[ex_ny][ex_nx] == 0:
                            exit_connected = True
                            break
                if exit_connected:
                    continue

            if maze[ny][nx] == 1 or is_exit or is_entry:
                if not is_exit:
                    maze[ny][nx] = 0
                wx, wy = x + dx // 2, y + dy // 2
                maze[wy][wx] = 0

                if xvar and _config.ANIMATION == 1:
                    update_cell(xvar, wx, wy, 0, _config)
                    if not is_exit and not is_entry:
                        update_cell(xvar, nx, ny, 0, _config)
                    if hasattr(_config, 'DELAY') and _config.DELAY > 0:
                        time.sleep(_config.DELAY)
                        xvar.mlx.mlx_do_sync(xvar.mlx_ptr)

                backtrack(nx, ny, maze, width, height, _config, xvar)


def generate(maze: list[list[int]], _config: Config,
             xvar: XVar) -> list[list[int]]:
    """
    Initialize and execute the backtracking generation algorithm.

    Args:
        maze (list[list[int]]): The initial maze grid.
        _config (Config): Configuration object.
        xvar (XVar): Graphics context.

    Returns:
        list[list[int]]: The generated maze grid.
    """
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

    if maze[start_y][start_x] == 1:
        maze[start_y][start_x] = 0
        if xvar and _config.ANIMATION == 1:
            update_cell(xvar, start_x, start_y, 0, _config)

    backtrack(start_x, start_y, maze, w, h, _config, xvar)

    return maze
