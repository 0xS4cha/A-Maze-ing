#!/usr/bin/env python3

from ..config import Config
import random
import time
from ..utils.mlx_utils import XVar
from typing import List


def indexOfSet(sets, c) -> int:
    """
    Find the index of the set containing a specific cell.

    Args:
        sets (list): List of sets containing cell coordinates.
        c (list): The cell coordinate [row, col] to find.

    Returns:
        int: The index of the set containing the cell, or -1 if not found.
    """
    for i, s in enumerate(sets):
        if c in s:
            return i
    return -1


def is_blocked(maze: List[List[int]], r: int, c: int) -> bool:
    return maze[r][c] == 2


def generate(maze: List[List[int]], config: Config,
             xvar: XVar | None = None) -> List[List[int]]:
    """
    Generate a maze using Eller's algorithm.

    Args:
        maze (List[List[int]]): Initial maze grid.
        config (Config): Configuration object.
        xvar (XVar | None): Graphics context for visualization.

    Returns:
        List[List[int]]: The generated maze grid.
    """
    width = len(maze[0])
    height = len(maze)

    sets = []

    # initialize first row
    for j in range(1, width, 2):
        if not is_blocked(maze, 1, j):
            maze[1][j] = 0
            sets.append([[1, j]])

    for i in range(1, height, 2):
        # keep only current row cells
        for k in range(len(sets)):
            sets[k] = [c for c in sets[k] if c[0] == i]
        sets = [s for s in sets if s]

        # fill missing cells
        for j in range(1, width, 2):
            if is_blocked(maze, i, j):
                continue
            if indexOfSet(sets, [i, j]) == -1:
                maze[i][j] = 0
                sets.append([[i, j]])

        # horizontal joins
        j = 3
        while j < width:
            if is_blocked(maze, i, j - 1):
                j += 2
                continue

            left = [i, j - 2]
            right = [i, j]

            if is_blocked(maze, *left) or is_blocked(maze, *right):
                j += 2
                continue

            s1 = indexOfSet(sets, left)
            s2 = indexOfSet(sets, right)

            if s1 != s2:
                if i == height - 2 or random.randint(0, 1):
                    maze[i][j - 1] = 0
                    merged = sets.pop(max(s1, s2))
                    sets[min(s1, s2)].extend(merged)

            j += 2

        if i == height - 2:
            break

        # vertical continuation (forced)
        new_sets = []

        for current in sets:
            candidates = []
            for r, c in current:
                nr = r + 2
                if nr < height and not is_blocked(maze, r + 1, c) and not is_blocked(maze, nr, c):
                    candidates.append((r, c))

            if not candidates:
                continue

            chosen = random.choice(candidates)
            r, c = chosen
            maze[r + 1][c] = 0
            maze[r + 2][c] = 0
            new_set = [[r + 2, c]]

            for r, c in candidates:
                if random.randint(0, 1):
                    maze[r + 1][c] = 0
                    maze[r + 2][c] = 0
                    new_set.append([r + 2, c])

            new_sets.append(new_set)

        sets = new_sets

    return maze
