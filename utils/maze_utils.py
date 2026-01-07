import config
import algorithms.backtracking as backtracking
import algorithms.eller as eller
from utils.mlx_utils import render_maze_to_mlx
import exception
from resolve import resolve


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


def add_symbol(maze, symbol, sigma=None):
    maze_h = len(maze)
    maze_w = len(maze[0])
    sym_h = len(symbol)
    sym_w = len(symbol[0])
    y_start = (maze_h - sym_h) // 2
    x_start = (maze_w - sym_w) // 2
    for y in range(len(ft_symbol)):
        last_x = x_start
        for x in range(len(ft_symbol[y])):
            if sigma is not None and y == 14:
                maze[y_start][last_x] = 1
            else:
                if ft_symbol[y][x] == 2:
                    maze[y_start][last_x] = ft_symbol[y][x]
            last_x += 1
        y_start += 1


def print_maze(maze: list[list[int]], empty, full):
    for line in range(len(maze)):
        for column in range(len(maze[line])):
            if maze[line][column] == 0:
                print(empty, end="")
            elif maze[line][column] == 1:
                print(full, end="")
            elif maze[line][column] == 2:
                print(config.COLOR_FT + full + config.COLOR_RESET, end='')
            elif maze[line][column] == 3:
                print(config.COLOR_STARTING + full + config.COLOR_RESET,
                      end='')
            elif maze[line][column] == 4:
                print(config.COLOR_ENDING + full + config.COLOR_RESET, end='')
        print()


def generate_maze(_config: config.Config, xvar=None) -> bool:
    algo_list = [backtracking, eller]
    global maze
    maze = [[1 for _ in range(_config.WIDTH)] for _ in range(_config.HEIGHT)]
    if _config.WIDTH > len(ft_symbol[0]) and _config.HEIGHT > len(ft_symbol):
        add_symbol(maze, ft_symbol, _config.ALGORITHMS == 1)
    if _config.ANIMATION and xvar:
        render_maze_to_mlx(xvar.mlx, xvar.mlx_ptr, xvar.win_1, maze, _config,
                           xvar)
    result: list[list[int]] = algo_list[_config.ALGORITHMS].generate(maze,
                                                                     _config,
                                                                     xvar)
    entry_x, entry_y = _config.ENTRY
    exit_x, exit_y = _config.EXIT
    if (entry_x < 1 or entry_y < 1 or entry_x > _config.WIDTH - 2 or
        entry_y > _config.HEIGHT - 2) \
            or (entry_x == exit_x and entry_y == exit_y):
        raise exception.ConfigException("Invalid entry or exit position, \
outside the map")
    result[entry_y][entry_x] = 3
    result[exit_y][exit_x] = 4
    result[_config.HEIGHT - 1][23] = 1
    if _config.GRAPHIC == 0:
        print_maze(result, _config.EMPTY_CHAR, _config.FULL_CHAR)
    resolve((_config.ENTRY[0], _config.ENTRY[1]), 0, result, None, _config)
    return result
