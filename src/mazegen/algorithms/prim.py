#!/usr/bin/env python3
"""Prim's algorithm for maze generation."""

import random
import time
from ..utils.mlx_utils import XVar, update_cell
from ..utils.generate_utils import Bit_position, remove_wall
from ..config import Config
from typing import List


def generate(maze: List[List[int]], _config: Config,
             xvar: XVar) -> List[List[int]]:
    """
    Initialize and execute Prim's algorithm.

    Args:
        maze (List[List[int]]): The maze grid.
        _config (Config): Configuration object.
        xvar (XVar): Graphics context.

    Returns:
        List[List[int]]: The generated maze.
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
    except (ValueError, IndexError):
        entry_x, entry_y = 0, 0

    start_x = max(0, min(entry_x, w - 1))
    start_y = max(0, min(entry_y, h - 1))

    frontier = []

    def add_frontier(fx: int, fy: int) -> None:
        if not (maze[fy][fx] & Bit_position.VISITED.value):
            maze[fy][fx] |= Bit_position.VISITED.value
            if xvar and _config.ANIMATION == 1:
                update_cell(xvar, fx, fy, maze[fy][fx], _config)

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            nx, ny = fx + dx, fy + dy
            if 0 <= nx < w and 0 <= ny < h:
                if not (maze[ny][nx] & Bit_position.VISITED.value):
                    frontier.append((fx, fy, nx, ny))

    if not (maze[start_y][start_x] & Bit_position.VISITED.value):
        add_frontier(start_x, start_y)
    else:
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            nx, ny = start_x + dx, start_y + dy
            if 0 <= nx < w and 0 <= ny < h:
                if not (maze[ny][nx] & Bit_position.VISITED.value):
                    frontier.append((start_x, start_y, nx, ny))

    while frontier:
        idx = random.randrange(len(frontier))
        cx, cy, nx, ny = frontier.pop(idx)

        if not (maze[ny][nx] & Bit_position.VISITED.value):
            remove_wall(maze, cx, cy, nx, ny)
            if xvar and _config.ANIMATION == 1:
                update_cell(xvar, cx, cy, maze[cy][cx], _config)
                if hasattr(_config, 'DELAY') and _config.DELAY > 0:
                    time.sleep(_config.DELAY)
                    xvar.mlx.mlx_do_sync(xvar.mlx_ptr)

            add_frontier(nx, ny)

    return maze
