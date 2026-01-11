"""Maze generation utilities."""
import random
import secrets
from .. import config
from ..algorithms import stacking as stacking
from ..algorithms import prim as prim
from ..utils.mlx_utils import XVar, render_maze_to_mlx
from ..utils.generate_utils import Bit_position
from .. import exception
from ..resolve import resolve
from typing import List

maze: List[List[int]] = []

ft_symbol = [
    [16, 31, 31, 29, 16, 16, 16],
    [16, 31, 31, 31, 26, 26, 16],
    [16, 16, 16, 21, 16, 16, 16],
    [31, 31, 16, 21, 16, 18, 26],
    [31, 31, 16, 21, 16, 16, 16],
]


def maze_mold(maze: List[List[int]], _config: config.Config) -> None:
    maze.clear()
    full_connections = (Bit_position.NORTH.value | Bit_position.EAST.value |
                        Bit_position.SOUTH.value | Bit_position.WEST.value)
    for _ in range(_config.HEIGHT):
        maze.append([full_connections for _ in range(_config.WIDTH)])
    return maze


def add_symbol(maze: List[List[int]], symbol: List[List[int]]) -> None:
    """
    Embed a custom symbol (e.g., '42') into the maze.

    Args:
        maze (List[List[int]]): The maze grid.
        symbol (List[List[int]]): The symbol pattern to embed (bitmasks).
    """
    maze_h = len(maze)
    maze_w = len(maze[0])
    sym_h = len(symbol)
    sym_w = len(symbol[0])
    y_start = (maze_h - sym_h) // 2
    x_start = (maze_w - sym_w) // 2
    for y in range(len(symbol)):
        last_x = x_start
        for x in range(len(symbol[y])):
            if symbol[y][x] == 16:
                maze[y_start][last_x] = symbol[y][x]
            else:
                maze[y_start][last_x] = symbol[y][x] & (
                    ~Bit_position.VISITED.value)
            last_x += 1
        y_start += 1


def make_non_perfect(maze: list[list[int]], path: list[tuple[int, int]]):
    """
    Modify the maze to make it non-perfect.

    Removes a random wall adjacent to the solution path to create loops
    and ensure multiple possible paths exist.

    Args:
        maze (list[list[int]]): The maze grid.
        path (list[tuple[int, int]]): The solution path coordinates.
    """
    h = len(maze)
    w = len(maze[0])
    loops_added = 0
    target_loops = max(2, min(w, h) // 4)

    indices = list(range(len(path)))
    random.shuffle(indices)

    for i in indices:
        if loops_added >= target_loops:
            break
        cx, cy = path[i]
        neighbors = [
            (0, -1, Bit_position.NORTH.value, Bit_position.SOUTH.value),
            (1, 0, Bit_position.EAST.value, Bit_position.WEST.value),
            (0, 1, Bit_position.SOUTH.value, Bit_position.NORTH.value),
            (-1, 0, Bit_position.WEST.value, Bit_position.EAST.value)
        ]
        random.shuffle(neighbors)

        for dx, dy, bit_curr, bit_neigh in neighbors:
            nx, ny = cx + dx, cy + dy
            if not (0 <= nx < w and 0 <= ny < h):
                continue
            if not (maze[cy][cx] & bit_curr):
                maze[cy][cx] |= bit_curr
                maze[ny][nx] |= bit_neigh
                loops_added += 1
                break


def generate_maze(_config: config.Config, xvar: XVar) -> List[List[int]]:
    """
    Orchestrate the maze generation process.

    Initializes the maze, adds symbols, calls the selected algorithm,
    and validates entry/exit points.

    Args:
        _config (config.Config): The configuration object.
        xvar (XVar): The graphics context.

    Returns:
        List[List[int]]: The final generated maze.

    Raises:
        exception.ConfigException: If entry/exit points are invalid.
    """
    global maze
    xvar.show_path = False
    algo_list = {False: prim, True: stacking}
    xvar.path = []
    maze = maze_mold(maze, _config)
    add_symbol(maze, ft_symbol)
    entry_x, entry_y = _config.ENTRY
    exit_x, exit_y = _config.EXIT
    new_seed = secrets.token_hex(8)
    random.seed(new_seed)
    print(f"Maze Seed: {new_seed}")
    if maze[exit_y][exit_x] == 2:
        raise exception.ConfigException("Invalid entry or exit position, \
on the 42 symbol (unvalid path)")
    if _config.ANIMATION and xvar:
        render_maze_to_mlx(
            xvar.mlx,
            xvar.mlx_ptr,
            xvar.win_1,
            maze,
            _config,
            xvar
        )
    try:
        result = algo_list[_config.PERFECT].generate(
            maze,
            _config,
            xvar
        )
    except RecursionError:
        raise exception.MazeException("Grid too large\
for recursive algorithm.")
    if (entry_x < 1 or entry_y < 1 or entry_x > _config.WIDTH - 2 or
        entry_y > _config.HEIGHT - 2) \
            or (entry_x == exit_x and entry_y == exit_y):
        raise exception.ConfigException("Invalid entry or exit position, \
outside the map")
    path = resolve(
        (_config.ENTRY[0], _config.ENTRY[1]),
        0,
        result,
        None,
        _config,
        xvar
    )
    if not _config.PERFECT:
        make_non_perfect(result, xvar.path)
    if type(path) is not list:
        raise exception.MazeException("Could not find a valid path")
    return result
