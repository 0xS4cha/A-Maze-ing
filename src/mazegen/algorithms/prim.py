#!/usr/bin/env python3

import random
import time
from ..utils.mlx_utils import XVar, update_cell
from ..config import Config
from typing import List


def generate(maze: List[List[int]], config: Config,
             xvar: XVar | None = None) -> List[List[int]]:
    """
    Generate a maze using Randomized Prim's algorithm.

    Args:
        maze (List[List[int]]): Initial maze grid.
        config (Config): Configuration object.
        xvar (XVar | None): Graphics context for visualization.

    Returns:
        List[List[int]]: The generated maze grid.
    """
    width = len(maze[0])
    height = len(maze)

    def is_valid(x: int, y: int) -> bool:
        return (0 < x < width - 1) and (0 < y < height - 1)

    start_x, start_y = (1, 1)

    maze[start_y][start_x] = 0
    if xvar and config.ANIMATION:
        update_cell(xvar, start_x, start_y, 0, config)

    # candidates
    frontier: List[tuple[int, int]] = []

    def add_frontier(gx: int, gy: int) -> None:
        moves = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        for dx, dy in moves:
            nx, ny = gx + dx, gy + dy
            if is_valid(nx, ny) and (maze[ny][nx] != 0):
                frontier.append((nx, ny))

    add_frontier(start_x, start_y)

    while frontier:
        # pick a random cell from the frontier
        idx = random.randrange(len(frontier))
        cx, cy = frontier.pop(idx)

        # skip
        if maze[cy][cx] != 1:
            continue

        # find neighbors
        neighbors = []
        moves = [(0, 2), (0, -2), (2, 0), (-2, 0)]  # NSEW
        for dx, dy in moves:
            nx, ny = cx + dx, cy + dy
            wx, wy = cx + dx // 2, cy + dy // 2

            if is_valid(nx, ny) and maze[ny][nx] == 0:
                if maze[wy][wx] != 2:
                    neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)

            # wall between current and neighbor
            wx, wy = (cx + nx) // 2, (cy + ny) // 2

            maze[cy][cx] = 0
            maze[wy][wx] = 0

            if xvar and config.ANIMATION:
                update_cell(xvar, cx, cy, 0, config)
                update_cell(xvar, wx, wy, 0, config)
                if config.DELAY > 0:
                    time.sleep(config.DELAY)
                    xvar.mlx.mlx_do_sync(xvar.mlx_ptr)
            add_frontier(cx, cy)
    return maze
