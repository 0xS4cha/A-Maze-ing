#!/usr/bin/env python3

import random


def check_case(x, y, maze, width, height) -> None:
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        if 0 <= nx < height and 0 <= ny < width:
            if maze[nx][ny] == 0:
                maze[nx][ny] = 1
                wall_x = x + (dx // 2)
                wall_y = y + (dy // 2)
                maze[wall_x][wall_y] = 1
                check_case(nx, ny, maze, width, height)


def generate(_config) -> bool:
    print("Starting")
    global maze
    global node
    w = _config.WIDTH
    h = _config.HEIGHT
    maze = [[0 for _ in range(w)] for _ in range(h)]
    for row in range(h):
        for col in range(w):
            if row == 0 or row == h-1 or col == 0 or col == w-1:
                maze[row][col] = 1
    start_x, start_y = 1, 1
    maze[start_x][start_y] = 1
    check_case(start_x, start_y, maze, _config.WIDTH, _config.HEIGHT)
    return maze
