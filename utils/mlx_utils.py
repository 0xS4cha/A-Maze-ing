import config
import exception
import time


class XVar:
    def __init__(self):
        self.mlx = None
        self.mlx_ptr = None
        self.screen_w = 0
        self.screen_h = 0
        self.win_w = 0
        self.win_h = 0
        self.win_1 = None
        self.win_2 = None
        self.imgidx = 0
        # image fields
        self.img = None
        self.img_data = None
        self.img_bpp = 0
        self.img_sl = 0
        self.img_format = 0
        self.img_w = 0
        self.img_h = 0


def manage_close(xvar):
    xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)


def manage_key_simple(key, xvar):
    if key in (113, 27, 65307):
        xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)
        return 0
    return 0


def render_buttons(xvar):
    pass


def calculate_window_size(_config, screen_w, screen_h, ui_width=250):
    avail_w = (screen_w if screen_w else 1920) - ui_width
    avail_h = (screen_h if screen_h else 1080)

    scale_x = max(1, avail_w // _config.WIDTH)
    scale_y = max(1, avail_h // _config.HEIGHT)
    scale = min(scale_x, scale_y, 16)

    img_w = _config.WIDTH * scale
    img_h = _config.HEIGHT * scale

    # Total window size
    win_w = img_w + ui_width
    win_h = img_h

    return win_w, win_h, scale


def manage_expose(xvar):
    if xvar.img:
        xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, xvar.win_1, xvar.img,
                                         0, 0)


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

    if xvar.img:
        mlx.mlx_destroy_image(mlx_ptr, xvar.img)

    img = mlx.mlx_new_image(mlx_ptr, img_w, img_h)
    if not img:
        raise exception.ConfigException("Can't create MLX image for maze \
rendering")

    data, bpp, sl, fmt = mlx.mlx_get_data_addr(img)

    for my in range(_config.HEIGHT):
        for mx in range(_config.WIDTH):
            val = maze[my][mx]
            color = _config.COLORS.get(val, 0xFFFFFFFF)
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

    # draw_buttons(xvar)

    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, img, 0, 0)

    if hasattr(_config, 'DELAY') and _config.DELAY > 0:
        time.sleep(_config.DELAY)


def update_cell(xvar, mx, my, val, _config):
    if not xvar or not xvar.img_data:
        return

    screen_w = xvar.screen_w if xvar.screen_w else _config.WIDTH * 8
    screen_h = xvar.screen_h if xvar.screen_h else _config.HEIGHT * 8
    scale_x = max(1, screen_w // _config.WIDTH)
    scale_y = max(1, screen_h // _config.HEIGHT)
    scale = min(scale_x, scale_y, 16)

    color_int = _config.COLORS.get(val, 0xFFFFFFFF)
    color_bytes = color_int.to_bytes(4, 'little')

    # Modification du buffer
    data = xvar.img_data
    sl = xvar.img_sl
    start_y = my * scale
    start_x = mx * scale

    for dy in range(scale):
        py = start_y + dy
        row_off = py * sl
        for dx in range(scale):
            px = start_x + dx
            off = row_off + px * 4
            if off + 4 <= len(data):
                data[off:off+4] = color_bytes

    xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, xvar.win_1, xvar.img, 0, 0)
