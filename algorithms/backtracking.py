#!/usr/bin/env python3

import random


def backtrack(x, y, maze, width, height):
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        if 0 < nx < height - 1 and 0 < ny < width - 1:
            if maze[nx][ny] == 1:
                maze[nx][ny] = 0
                maze[x + dx // 2][y + dy // 2] = 0
                backtrack(nx, ny, maze, width, height)


def ensure_connectivity(maze, width, height):
    for row in range(1, height - 1, 2):
        for col in range(1, width - 1, 2):
            if maze[row][col] == 1:
                neighbors = [(row - 2, col), (row + 2, col), (row, col - 2), (row, col + 2)]
                random.shuffle(neighbors)
                for nx, ny in neighbors:
                    if 0 <= nx < height and 0 <= ny < width and maze[nx][ny] == 0:
                        maze[row][col] = 0
                        maze[(row + nx) // 2][(col + ny) // 2] = 0
                        backtrack(row, col, maze, width, height)
                        break


def generate(maze, _config):
    print("Starting")
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

    entry_x = max(0, min(entry_x, h - 1))
    entry_y = max(0, min(entry_y, w - 1))
    exit_x = max(0, min(exit_x, h - 1))
    exit_y = max(0, min(exit_y, w - 1))

    start_x = max(1, min(entry_x, h - 2))
    start_y = max(1, min(entry_y, w - 2))
    if start_x % 2 == 0:
        start_x += 1 if start_x < h - 2 else -1
    if start_y % 2 == 0:
        start_y += 1 if start_y < w - 2 else -1

    maze[start_x][start_y] = 0
    backtrack(start_x, start_y, maze, w, h)

    ensure_connectivity(maze, w, h)

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
