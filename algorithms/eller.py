#!/usr/bin/env python3

from config import Config
import random


def generate(config: Config):
    width = config.WIDTH // 2
    height = config.HEIGHT // 2
    next_id = 0
    sets = [i for i in range(width)]
    next_id = width

    maze = [
        [{'R': False, 'D': False} for _ in range(width)]
        for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if sets[x] is None:
                sets[x] = next_id
                next_id += 1

        # horizontal connections
        for x in range(width - 1):
            if sets[x] != sets[x + 1] and (y == height - 1 or random.choice([True, False])):
                maze[y][x]['R'] = True
                old = sets[x + 1]
                new = sets[x]
                for i in range(width):
                    if sets[i] == old:
                        sets[i] = new

        # force merge for last row
        if y == height - 1:
            break

        # vertical connections
        next_sets = [None] * width
        used = {}
        for x in range(width):
            used.setdefault(sets[x], []).append(x)

        for s in used:
            cells = used[s]
            random.shuffle(cells)
            count = random.randint(1, len(cells))  # one random cell vertical
            for x in cells[:count]:
                maze[y][x]['D'] = True
                next_sets[x] = sets[x]
        sets = next_sets

    pw = width * 2 + 1
    ph = height * 2 + 1

    pixels = [[1] * pw for _ in range(ph)]

    for y in range(height):
        for x in range(width):
            px = x * 2 + 1
            py = y * 2 + 1
            pixels[py][px] = 0
            if maze[y][x]['R']:
                pixels[py][px + 1] = 0
            if maze[y][x]['D']:
                pixels[py + 1][px] = 0
    return pixels
