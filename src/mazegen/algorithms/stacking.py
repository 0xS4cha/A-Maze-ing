#!/usr/bin/env python3
"""Recursive backtracking algorithm for maze generation."""

import random
import time
from ..utils.mlx_utils import XVar, update_cell
from ..utils.generate_utils import remove_wall, Bit_position
from ..config import Config
from typing import List


def get_unvisited_neighbors(x: int, y: int, maze: List[List[int]],
                            width: int, height: int) -> List[tuple[int, int]]:
    """Return a list of unvisited neighbors."""
    neighbors = []
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            if not (maze[ny][nx] & Bit_position.VISITED.value):
                neighbors.append((nx, ny))
    return neighbors


def stacking(x: int, y: int, maze: List[List[int]], width: int, height: int,
             _config: Config, xvar: XVar) -> None:
    """
    Generate a maze using the iterative algorithm with stack.
    """
    stack = [(x, y)]
    maze[y][x] |= Bit_position.VISITED.value

    if xvar and _config.ANIMATION == 1:
        update_cell(xvar, x, y, maze[y][x], _config)
        if hasattr(_config, 'DELAY') and _config.DELAY > 0:
            time.sleep(_config.DELAY)
            xvar.mlx.mlx_do_sync(xvar.mlx_ptr)

    while stack:
        cx, cy = stack[-1]
        neighbors = get_unvisited_neighbors(cx, cy, maze, width, height)

        if neighbors:
            nx, ny = random.choice(neighbors)
            remove_wall(maze, cx, cy, nx, ny)
            maze[ny][nx] |= Bit_position.VISITED.value
            if xvar and _config.ANIMATION == 1:
                update_cell(xvar, cx, cy, maze[cy][cx], _config)
                update_cell(xvar, nx, ny, maze[ny][nx], _config)
                if hasattr(_config, 'DELAY') and _config.DELAY > 0:
                    time.sleep(_config.DELAY)
                    xvar.mlx.mlx_do_sync(xvar.mlx_ptr)
            stack.append((nx, ny))
        else:
            stack.pop()


def generate(maze: List[List[int]], _config: Config,
             xvar: XVar) -> List[List[int]]:
    """
    Initialize and execute the backtracking generation algorithm.
    """
    w = _config.WIDTH
    h = _config.HEIGHT

    for y in range(h):
        for x in range(w):
            if not (maze[y][x] & Bit_position.VISITED.value):
                maze[y][x] = 0

    try:
        entry_x = int(_config.ENTRY[0])
        entry_y = int(_config.ENTRY[1])
        # exit_x = int(_config.EXIT[0])
        # exit_y = int(_config.EXIT[1])
    except (ValueError, IndexError):
        entry_x, entry_y = 0, 0

    start_x = max(0, min(entry_x, w - 1))
    start_y = max(0, min(entry_y, h - 1))

    stacking(start_x, start_y, maze, w, h, _config, xvar)

    return maze
