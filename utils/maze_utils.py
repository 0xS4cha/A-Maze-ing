import config
import algorithms.backtracking as backtracking
import algorithms.eller as eller
import exception


ft_symbol = [
    [2, 0, 0, 0, 2, 2, 2],
    [2, 0, 0, 0, 0, 0, 2],
    [2, 2, 2, 0, 2, 2, 2],
    [0, 0, 2, 0, 2, 0, 0],
    [0, 0, 2, 0, 2, 2, 2],
]


def add_symbol(maze, symbol):
    x_starting = int(len(maze[0]) / 2 - len(ft_symbol[0]))
    y_starting = int(len(maze) / 2 - len(ft_symbol))
    for y in range(len(ft_symbol)):
        last_x = x_starting
        for x in range(len(ft_symbol[y])):
            maze[y_starting][last_x] = ft_symbol[y][x]
            last_x += 1
        y_starting += 1
    return maze


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


def generate_maze(_config: config.Config) -> bool:
    algo_list = [backtracking, eller]
    result: list[list[int]] = algo_list[_config.ALGORITHMS].generate(_config)
    # set entry and exit
    entry_x, entry_y = _config.ENTRY
    exit_x, exit_y = _config.EXIT
    if (entry_x < 1 or entry_y < 1 or entry_x > _config.WIDTH - 2 or
        entry_y > _config.HEIGHT - 2) \
            or (entry_x == exit_x and entry_y == exit_y):
        raise exception.ConfigException("Invalid entry or exit position, \
outside the map")
    result[entry_y][entry_x] = 3
    result[exit_y][exit_x] = 4
    if _config.WIDTH > len(ft_symbol[0]) and _config.HEIGHT > len(ft_symbol):
        result = add_symbol(result, ft_symbol)
    print_maze(result, _config.EMPTY_CHAR, _config.FULL_CHAR)
    return True
