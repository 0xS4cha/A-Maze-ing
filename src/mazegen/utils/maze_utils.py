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
    h = len(maze)
    w = len(maze[0])

    def in_bounds(r, c):
        return 0 <= r < h and 0 <= c < w

    def creates_2x2(r, c):
        for dr in (-1, 0):
            for dc in (-1, 0):
                cells = [
                    (r + dr, c + dc),
                    (r + dr + 1, c + dc),
                    (r + dr, c + dc + 1),
                    (r + dr + 1, c + dc + 1),
                ]
                if all(in_bounds(rr, cc) and maze[rr][cc] == 0 for rr, cc in cells):
                    return True
        return False

    for i in range(2, len(path) - 2):
        r, c = path[i]
        pr, pc = path[i - 1]
        nr, nc = path[i + 1]

        dr, dc = nr - r, nc - c

        # only allow straight cardinal paths
        if abs(dr) + abs(dc) != 1:
            continue

        # perpendicular directions (strict)
        for pdr, pdc in ((dc, -dr), (-dc, dr)):
            r1, c1 = r + pdr, c + pdc
            r2, c2 = r1 + dr, c1 + dc

            if not in_bounds(r1, c1) or not in_bounds(r2, c2):
                continue

            if maze[r1][c1] != 1 or maze[r2][c2] != 1:
                continue

            # simulate carve
            maze[r1][c1] = 0
            maze[r2][c2] = 0

            if creates_2x2(r1, c1) or creates_2x2(r2, c2):
                maze[r1][c1] = 1
                maze[r2][c2] = 1
                continue

            # remove original cell to keep acyclic
            maze[r][c] = 1
            return


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
    algo_list = [prim, backtracking]
    xvar.path = []
    maze = [[1 for _ in range(_config.WIDTH)] for _ in range(_config.HEIGHT)]
    add_symbol(maze, ft_symbol)
    entry_x, entry_y = _config.ENTRY
    exit_x, exit_y = _config.EXIT
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
    make_non_perfect(result, xvar.path)
    if type(path) is not list:
        raise exception.MazeException("Could not find a valid path")
    return result
