import random
import secrets
from .. import config
from ..algorithms import backtracking as backtracking
from ..algorithms import prim as prim
from ..utils.mlx_utils import XVar, render_maze_to_mlx
from .. import exception
from ..resolve import resolve
from typing import List

maze: List[List[int]] = []
ft_symbol = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 0, 0, 2, 2, 2, 2, 2],
    [0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def add_symbol(maze: List[List[int]], symbol: List[List[int]]) -> None:
    """
    Embed a custom symbol (e.g., '42') into the maze.

    Args:
        maze (List[List[int]]): The maze grid.
        symbol (List[List[int]]): The symbol pattern to embed.
    """
    maze_h = len(maze)
    maze_w = len(maze[0])
    sym_h = len(symbol)
    sym_w = len(symbol[0])
    y_start = (maze_h - sym_h) // 2
    x_start = (maze_w - sym_w) // 2
    for y in range(len(ft_symbol)):
        last_x = x_start
        for x in range(len(ft_symbol[y])):
            if y == 14:
                maze[y_start][last_x] = 1
            else:
                if ft_symbol[y][x] == 2:
                    maze[y_start][last_x] = ft_symbol[y][x]
            last_x += 1
        y_start += 1


def make_non_perfect(maze: list[list[int]], path: list[tuple[int, int]]):
    """
    Modify the maze to make it non-perfect by removing random walls adjacent\
to the solution path.
    This creates loops and ensures multiple possible paths exist.
    """
    h = len(maze)
    w = len(maze[0])
    loops_added = 0
    target_loops = 4  # Ensure at least a few loops

    # Try random points along the path
    indices = list(range(len(path)))
    random.shuffle(indices)

    for i in indices:
        if loops_added >= target_loops:
            break

        c, r = path[i]

        # check for adjacent wall to remove
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(moves)

        for dc, dr in moves:
            wc, wr = c + dc, r + dr        # wall
            nc, nr = c + 2*dc, r + 2 * dr  # neighbor

            if not (0 < wc < w-1 and 0 < wr < h-1):
                continue
            if not (0 < nc < w-1 and 0 < nr < h-1):
                continue

            if maze[wr][wc] == 1:
                if maze[nr][nc] == 0:
                    maze[wr][wc] = 0
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
    algo_list = [prim, backtracking]
    xvar.path = []
    maze = [[1 for _ in range(_config.WIDTH)] for _ in range(_config.HEIGHT)]
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
    result: list[list[int]] = algo_list[_config.PERFECT].generate(
        maze,
        _config,
        xvar
    )
    if (entry_x < 1 or entry_y < 1 or entry_x > _config.WIDTH - 2 or
        entry_y > _config.HEIGHT - 2) \
            or (entry_x == exit_x and entry_y == exit_y):
        raise exception.ConfigException("Invalid entry or exit position, \
outside the map")
    result[entry_y][entry_x] = 3
    result[exit_y][exit_x] = 4
    path = resolve(
        (_config.ENTRY[0], _config.ENTRY[1]),
        0,
        result,
        None,
        _config,
        xvar
    )
    if (_config.PERFECT == 0):
        make_non_perfect(result, xvar.path)
    if type(path) is not list:
        raise exception.MazeException("Could not find a valid path")
    return result
