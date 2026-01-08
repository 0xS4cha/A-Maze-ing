#!/usr/bin/env python3

from config import Config
import random
import time
from utils.mlx_utils import update_cell


def generate(maze, config: Config, xvar=None):
    w = config.WIDTH
    h = config.HEIGHT

    width = (w - 1) // 2
    height = (h - 1) // 2

    sets = [i for i in range(width)]
    next_id = width

    def blocked(r, c):
        return maze[r][c] == 2

    def draw_update(r, c):
        if xvar:
            update_cell(xvar, c, r, 0, config)
            if hasattr(config, 'DELAY') and config.DELAY > 0:
                time.sleep(config.DELAY)
                xvar.mlx.mlx_do_sync(xvar.mlx_ptr)

    for y in range(height):
        new_sets = set()
        for x in range(width):
            ry, rx = 2 * y + 1, 2 * x + 1
            if blocked(ry, rx):
                sets[x] = None
                continue
            if sets[x] is None:
                sets[x] = next_id
                new_sets.add(next_id)
                next_id += 1
            maze[ry][rx] = 0
            draw_update(ry, rx)

        # horizontal connections
        for x in range(width - 1):
            ry, rx = 2 * y + 1, 2 * x + 2
            if blocked(ry, rx):
                continue
            if sets[x] is not None and sets[x + 1] is not None:
                if sets[x] != sets[x + 1]:
                    if (y == height - 1
                            or sets[x] in new_sets
                            or sets[x + 1] in new_sets
                            or random.choice([0, 1])):
                        maze[ry][rx] = 0
                        draw_update(ry, rx)
                        old = sets[x + 1]
                        new = sets[x]
                        for i in range(width):
                            if sets[i] == old:
                                sets[i] = new
                elif not config.PERFECT and random.choice([0, 1]):
                    maze[ry][rx] = 0
                    draw_update(ry, rx)

        # vertical connections
        if y < height - 1:
            next_sets = [None] * width
            used = {}
            for x in range(width):
                if sets[x] is not None:
                    used.setdefault(sets[x], []).append(x)

            for s, cells in used.items():
                random.shuffle(cells)
                count = random.randint(1, len(cells))
                if not config.PERFECT:
                    count = random.randint(1, len(cells)) if random.choice([0, 1]) else len(cells)

                for x in cells[:count]:
                    ry, rx = 2 * y + 2, 2 * x + 1
                    if blocked(ry, rx):
                        continue
                    maze[ry][rx] = 0
                    draw_update(ry, rx)
                    next_sets[x] = s
            sets = next_sets

    entry_x, entry_y = tuple(getattr(config, "ENTRY", (1, 1)))
    exit_x, exit_y = tuple(getattr(config, "EXIT", (h - 2, w - 2)))

    maze[entry_x][entry_y] = 0
    maze[exit_x][exit_y] = 0

    for r in range(h):
        for c in range(w):
            if maze[r][c] == 2:
                continue
            if r == 0 or r == h - 1 or c == 0 or c == w - 1:
                if (r, c) not in [(entry_x, entry_y), (exit_x, exit_y)]:
                    maze[r][c] = 1
    return maze
