from .. import config
from ..algorithms import backtracking as backtracking
from ..algorithms import eller as eller
from ..parser import generate_output
from ..utils.mlx_utils import render_maze_to_mlx
from .. import exception
from ..resolve import resolve


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


def add_symbol(maze: list[list[int]], symbol: list[list[int]],
               is_perfect: bool) -> None:
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

    if not is_perfect:
        logo_x = len(maze[0]) // 2 - len(ft_symbol[0]) // 2
        logo_y = len(maze) // 2 - len(ft_symbol) // 2

        maze[logo_y][logo_x + 12] = 0
        maze[logo_y + 1][logo_x + 12] = 0
        maze[logo_y + 2][logo_x + 12] = 0


def generate_maze(_config: config.Config, xvar=None) -> bool:
    global maze
    algo_list = [eller, backtracking]
    xvar.path = []
    maze = [[1 for _ in range(_config.WIDTH)] for _ in range(_config.HEIGHT)]
    add_symbol(maze, ft_symbol, _config.PERFECT == 1)
    entry_x, entry_y = _config.ENTRY
    exit_x, exit_y = _config.EXIT
    if maze[exit_y][exit_x] == 2:
        raise exception.ConfigException("Invalid entry or exit position, \
on the 42 symbol (unvalid path)")
    if _config.ANIMATION and xvar:
        render_maze_to_mlx(xvar.mlx, xvar.mlx_ptr, xvar.win_1, maze, _config,
                           xvar)
    result: list[list[int]] = algo_list[_config.PERFECT].generate(maze,
                                                                  _config,
                                                                  xvar)
    if (entry_x < 1 or entry_y < 1 or entry_x > _config.WIDTH - 2 or
        entry_y > _config.HEIGHT - 2) \
            or (entry_x == exit_x and entry_y == exit_y):
        raise exception.ConfigException("Invalid entry or exit position, \
outside the map")
    result[entry_y][entry_x] = 3
    result[exit_y][exit_x] = 4
    result[_config.HEIGHT - 1][23] = 1
    path = resolve(
        (_config.ENTRY[0], _config.ENTRY[1]),
        0,
        result,
        None,
        _config,
        xvar
    )
    if type(path) is list:
        generate_output(result, path, _config)
    else:
        exception.display_errors("Could not find a valid path")
    return result
