#!/usr/bin/env python3

import math
from ..config import Config
import random
import time
from ..utils.mlx_utils import XVar, update_cell
from typing import List


def indexOfSet(sets, c) -> int:
    for i, s in enumerate(sets):
        if c in s:
            return i
    return -1


def generate(maze: List[List[int]], config: Config,
             xvar: XVar | None = None) -> List[List[int]]:

    width = len(maze[0])
    height = len(maze)

    sets: List[List[List[int]]] = []
    for j in range(1, width, 2):
        if maze[1][j] != 2:
            maze[1][j] = 0
            sets.append([[1, j]])

    for i in range(1, height, 2):
        # clear sets
        for m in range(len(sets)):
            sets[m] = [c for c in sets[m] if c[0] == i]
        sets = [s for s in sets if s]

        # fill empty spots
        for j in range(1, width, 2):
            if maze[i][j] == 2:
                continue
            if indexOfSet(sets, [i, j]) == -1:
                sets.append([[i, j]])
                maze[i][j] = 0

        # horizontal joins
        for j in range(3, width, 2):
            if maze[i][j] == 2 or maze[i][j - 1] == 2 or maze[i][j - 2] == 2:
                continue

            set1 = indexOfSet(sets, [i, j - 2])
            set2 = indexOfSet(sets, [i, j])

            should_join = False
            if set1 != set2:
                join = 1 if i == height - 2 else random.randint(0, 1)
                should_join = bool(join)
            elif i != height - 2 and random.randint(0, 100) < 5:
                should_join = True
            
            if should_join:
                maze[i][j - 1] = 0
                if set1 != set2:
                    removed = sets.pop(set2)
                    if set2 < set1:
                        set1 -= 1
                    sets[set1].extend(removed)

        if i == height - 2:
            break

        # vertical connections
        initial_len = len(sets)
        for j in range(initial_len):
            current = sets[j]
            cells = [c for c in current if c[0] == i]
            
            if not cells:
                continue

            continued = False
            valid_extensions = []

            for cell in cells:
                next_r = cell[0] + 2
                wall_r = cell[0] + 1
                c = cell[1]

                if next_r >= height:
                    continue
                if maze[wall_r][c] == 2 or maze[next_r][c] == 2:
                    continue
                
                valid_extensions.append(cell)
                msg = random.randint(0, 1)
                if msg:
                    continued = True
                    current.append([next_r, c])
                    maze[wall_r][c] = 0
                    maze[next_r][c] = 0
            
            if not continued and valid_extensions:
                chosen = random.choice(valid_extensions)
                r, c = chosen[0], chosen[1]
                current.append([r + 2, c])
                maze[r + 1][c] = 0
                maze[r + 2][c] = 0

    # Post-processing 1: Remove isolated walls (floating walls)
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if maze[i][j] == 1:
                if (maze[i - 1][j] == 0 and maze[i + 1][j] == 0 and
                        maze[i][j - 1] == 0 and maze[i][j + 1] == 0):
                    maze[i][j] = 0

    # Post-processing 2: Remove 2x2 wall blocks (prevent full areas)
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if (maze[i][j] == 1 and maze[i + 1][j] == 1 and
                    maze[i][j + 1] == 1 and maze[i + 1][j + 1] == 1):
                maze[i][j] = 0

    # Post-processing 3: remove 3x3 empty areas by filling center
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if maze[i][j] == 0:
                is_3x3 = True
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        if maze[i + di][j + dj] != 0:
                            is_3x3 = False
                            break
                    if not is_3x3:
                        break
                if is_3x3:
                    maze[i][j] = 1

    # Post-processing 4: Remove isolated empty cells (keep largest component)
    visited = set()
    components = []
    for i in range(height):
        for j in range(width):
            if maze[i][j] == 0 and (i, j) not in visited:
                comp = []
                stack = [(i, j)]
                visited.add((i, j))
                while stack:
                    r, c = stack.pop()
                    comp.append((r, c))
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < height and 0 <= nc < width:
                            if maze[nr][nc] == 0 and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                stack.append((nr, nc))
                components.append(comp)

    if components:
        largest_comp = max(components, key=len)
        for comp in components:
            if comp != largest_comp:
                for r, c in comp:
                    maze[r][c] = 1

    return maze
