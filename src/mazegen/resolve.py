#!/usr/bin/env python3

from .config import Config
from collections import deque
from .utils.mlx_utils import XVar


def resolve(pos: tuple[int, int], direction: int,
            maze: list[list[int]],
            visited: list[list[bool]] | None,
            config: Config, xvar: XVar) -> list[str] | bool:
    queue = deque([pos])
    visited_set = {pos}
    came_from: dict[tuple[int, int], tuple[int, int] | None] = {pos: None}
    end_pos = tuple(config.EXIT)

    final_node: tuple[int, int] | None = None

    while queue:
        current = queue.popleft()

        if current == end_pos:
            final_node = current
            break

        x, y = current
        # Directions: N, E, S, W
        movements = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        for dx, dy in movements:
            nx, ny = x + dx, y + dy

            if not (0 <= nx < config.WIDTH and 0 <= ny < config.HEIGHT):
                continue

            if maze[ny][nx] == 1 or maze[ny][nx] == 2:
                continue

            if (nx, ny) not in visited_set:
                visited_set.add((nx, ny))
                came_from[(nx, ny)] = current
                queue.append((nx, ny))

    if final_node:
        path = []
        curr = final_node
        while curr != pos:
            parent = came_from[curr]
            if parent is None:
                break
            dx, dy = curr[0] - parent[0], curr[1] - parent[1]

            d = ""
            if dx == 0 and dy == -1:
                d = "N"
            elif dx == 1 and dy == 0:
                d = "E"
            elif dx == 0 and dy == 1:
                d = "S"
            elif dx == -1 and dy == 0:
                d = "W"
            path.append(d)

            if curr != end_pos:
                xvar.path.append((curr[0], curr[1]))
            curr = parent
        path.reverse()
        return path
    return False
