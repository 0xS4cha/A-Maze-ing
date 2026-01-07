import config
import algorithms.backtracking as backtracking
import algorithms.eller as eller
import exception

                
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


def add_symbol(maze, symbol):
    maze_h = len(maze)
    maze_w = len(maze[0])
    sym_h = len(symbol)
    sym_w = len(symbol[0])

    y_start = (maze_h - sym_h) // 2
    x_start = (maze_w - sym_w) // 2
    for y in range(len(ft_symbol)):
        last_x = x_start
        for x in range(len(ft_symbol[y])):
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


def generate_maze(_config: config.Config) -> bool:
    algo_list = [backtracking, eller]
    global maze
    maze = [[1 for _ in range(_config.WIDTH)] for _ in range(_config.HEIGHT)]
    if _config.WIDTH > len(ft_symbol[0]) and _config.HEIGHT > len(ft_symbol):
        add_symbol(maze, ft_symbol)
    result: list[list[int]] = algo_list[_config.ALGORITHMS].generate(maze,
                                                                     _config)
    entry_x, entry_y = _config.ENTRY
    exit_x, exit_y = _config.EXIT
    if (entry_x < 1 or entry_y < 1 or entry_x > _config.WIDTH - 2 or
        entry_y > _config.HEIGHT - 2) \
            or (entry_x == exit_x and entry_y == exit_y):
        raise exception.ConfigException("Invalid entry or exit position, \
outside the map")
    result[entry_y][entry_x] = 3
    result[exit_y][exit_x] = 4
    if not _config.GRAPHIC:
        print_maze(result, _config.EMPTY_CHAR, _config.FULL_CHAR)
    return result


def render_maze_to_mlx(mlx, mlx_ptr, win_ptr, maze: list[list[int]], _config:
                       config.Config, xvar):
    try:
        screen_w = xvar.screen_w if xvar.screen_w else _config.WIDTH * 8
        screen_h = xvar.screen_h if xvar.screen_h else _config.HEIGHT * 8
    except Exception:
        screen_w = _config.WIDTH * 8
        screen_h = _config.HEIGHT * 8

    scale_x = max(1, screen_w // _config.WIDTH)
    scale_y = max(1, screen_h // _config.HEIGHT)
    scale = min(scale_x, scale_y, 16)

    img_w = _config.WIDTH * scale
    img_h = _config.HEIGHT * scale

    img = mlx.mlx_new_image(mlx_ptr, img_w, img_h)
    if not img:
        raise exception.ConfigException("Can't create MLX image for maze \
rendering")

    data, bpp, sl, fmt = mlx.mlx_get_data_addr(img)

    COLORS = {
        0: 0xFF1E1E2E,  # empty -> Dark Blue/Black background (Base)
        1: 0xFF45475A,  # wall -> Soft Grey/Blue (Surface)
        2: 0xFFF9E2AF,  # ft symbol -> Gold/Yellow (Accent principal)
        3: 0xFFA6E3A1,  # start -> Soft Green
        4: 0xFFF38BA8,  # end -> Soft Red
    }

    for my in range(_config.HEIGHT):
        for mx in range(_config.WIDTH):
            val = maze[my][mx]
            color = COLORS.get(val, 0xFFFFFFFF)
            for dy in range(scale):
                py = my * scale + dy
                row_off = py * sl
                for dx in range(scale):
                    px = mx * scale + dx
                    off = row_off + px * 4
                    if off + 4 <= len(data):
                        data[off:off+4] = (color).to_bytes(4, 'little')

    xvar.img = img
    xvar.img_data = data
    xvar.img_bpp = bpp
    xvar.img_sl = sl
    xvar.img_format = fmt
    xvar.img_w = img_w
    xvar.img_h = img_h

    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, img, 0, 0)
