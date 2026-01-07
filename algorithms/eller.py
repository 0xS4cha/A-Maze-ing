#!/usr/bin/env python3

from config import Config
import random
import time
from utils.mlx_utils import render_maze_to_mlx, update_cell


def generate(maze, config: Config, xvar=None):
    w = config.WIDTH
    h = config.HEIGHT

    width = (w - 1) // 2
    height = (h - 1) // 2

    sets = [i for i in range(width)]
    next_id = width

    def draw_update(r, c):
        if xvar:
            update_cell(xvar, c, r, 0, config)
            if hasattr(config, 'DELAY') and config.DELAY > 0:
                time.sleep(config.DELAY)
                xvar.mlx.mlx_do_sync(xvar.mlx_ptr)

    for y in range(height):
        for x in range(width):
            if sets[x] is None:
                sets[x] = next_id
                next_id += 1
            # Carve cell
            maze[2 * y + 1][2 * x + 1] = 0
            draw_update(2 * y + 1, 2 * x + 1)

        # horizontal connections
        for x in range(width - 1):
            if sets[x] != sets[x + 1] and (y == height - 1 or random.choice([True, False])):
                maze[2 * y + 1][2 * x + 2] = 0
                draw_update(2 * y + 1, 2 * x + 2)
                old = sets[x + 1]
                new = sets[x]
                for i in range(width):
                    if sets[i] == old:
                        sets[i] = new

        # vertical connections
        if y < height - 1:
            next_sets = [None] * width
            used = {}
            for x in range(width):
                used.setdefault(sets[x], []).append(x)

            for s in used:
                cells = used[s]
                random.shuffle(cells)
                count = random.randint(1, len(cells))
                for x in cells[:count]:
                    maze[2 * y + 2][2 * x + 1] = 0
                    draw_update(2 * y + 2, 2 * x + 1)
                    next_sets[x] = sets[x]
            sets = next_sets

    try:
        entry_x = int(config.ENTRY[0])
        entry_y = int(config.ENTRY[1])
        exit_x = int(config.EXIT[0])
        exit_y = int(config.EXIT[1])
    except (ValueError, IndexError):
        entry_x, entry_y = 1, 1
        exit_x, exit_y = h - 2, w - 2

    entry_x = max(0, min(entry_x, h - 1))
    entry_y = max(0, min(entry_y, w - 1))
    exit_x = max(0, min(exit_x, h - 1))
    exit_y = max(0, min(exit_y, w - 1))

    maze[entry_x][entry_y] = 0
    if entry_x == 0 and entry_x + 1 < h:
        maze[entry_x + 1][entry_y] = 0
    elif entry_x == h - 1 and entry_x - 1 >= 0:
        maze[entry_x - 1][entry_y] = 0
    elif entry_y == 0 and entry_y + 1 < w:
        maze[entry_x][entry_y + 1] = 0
    elif entry_y == w - 1 and entry_y - 1 >= 0:
        maze[entry_x][entry_y - 1] = 0

    maze[exit_x][exit_y] = 0
    if exit_x == 0 and exit_x + 1 < h:
        maze[exit_x + 1][exit_y] = 0
    elif exit_x == h - 1 and exit_x - 1 >= 0:
        maze[exit_x - 1][exit_y] = 0
    elif exit_y == 0 and exit_y + 1 < w:
        maze[exit_x][exit_y + 1] = 0
    elif exit_y == w - 1 and exit_y - 1 >= 0:
        maze[exit_x][exit_y - 1] = 0

    for row in range(h):
        for col in range(w):
            if row == 0 or row == h - 1 or col == 0 or col == w - 1:
                is_entry = (row == entry_x and col == entry_y)
                is_exit = (row == exit_x and col == exit_y)
                if not is_entry and not is_exit:
                    maze[row][col] = 1
                else:
                    maze[row][col] = 0
    return maze
