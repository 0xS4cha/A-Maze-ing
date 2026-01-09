from .. import config
from .. import exception
from mlx import Mlx
import time
from typing import Any, List


class XVar:
    """
    Class to hold X window server variables and MLX state.
    """
    def __init__(self) -> None:
        self.mlx: Any = None
        self.mlx_ptr = None
        self.screen_w = 0
        self.screen_h = 0
        self.win_w = 0
        self.win_h = 0
        self.win_1 = None
        self.win_2 = None
        self.imgidx = 0
        self.color_palette = 0
        self.maze_data: List[List[int]] = []
        self.path: List[tuple[int, int]] = []
        self.show_path = False
        self.img = None
        self.img_data = None
        self.img_bpp = 0
        self.img_sl = 0
        self.img_format = 0
        self.img_w = 0
        self.img_h = 0


def manage_close(xvar: XVar) -> None:
    """
    Callback to handle window close event.

    Args:
        xvar (XVar): The graphics context.
    """
    xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)


def manage_key_simple(key: int, xvar: XVar) -> None:
    """
    Simple key handler for closing the window with 'q' or ESC.

    Args:
        key (int): The key code pressed.
        xvar (XVar): The graphics context.
    """
    if key in (113, 27, 65307):
        xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)
        return
    return


def calculate_window_size(_config: config.Config, screen_w: int, screen_h: int,
                          ui_width: int = 250) -> tuple[int, int, int]:
    """
    Calculate the appropriate window size and cell size based on screen size.

    Args:
        _config (config.Config): The configuration using maze dimensions.
        screen_w (int): The width of the screen.
        screen_h (int): The height of the screen.
        ui_width (int): Width reserved for the UI panel.

    Returns:
        tuple[int, int, int]: A tuple containing (required_width, required_height, cell_size).
    """
    avail_w = (screen_w if screen_w else 1920) - ui_width
    avail_h = (screen_h if screen_h else 1080)

    scale_x = max(1, avail_w // _config.WIDTH)
    scale_y = max(1, avail_h // _config.HEIGHT)
    scale = min(scale_x, scale_y, 16)

    img_w = _config.WIDTH * scale
    img_h = _config.HEIGHT * scale

    win_w = img_w + ui_width
    win_h = img_h

    return win_w, win_h, scale


def manage_expose(xvar: XVar) -> None:
    """
    Manage the expose event to render the image.

    Args:
        xvar (XVar): The graphics context.
    """
    if xvar.img:
        xvar.mlx.mlx_put_image_to_window(
            xvar.mlx_ptr,
            xvar.win_1,
            xvar.img,
            0,
            0
        )


def render_maze_to_mlx(mlx: Mlx, mlx_ptr: Any, win_ptr: Any,
                       maze: List[List[int]],
                       _config: config.Config, xvar: XVar) -> None:
    """
    Render the maze to the MLX window.

    Args:
        mlx (Mlx): The MLX instance.
        mlx_ptr (Any): The MLX pointer.
        win_ptr (Any): The window pointer.
        maze (List[List[int]]): The maze data.
        _config (config.Config): The configuration instance.
        xvar (XVar): The graphics context.
    """
    try:
        screen_w = xvar.screen_w if xvar.screen_w else 1920
        screen_h = xvar.screen_h if xvar.screen_h else 1080
    except Exception:
        screen_w = 1920
        screen_h = 1080

    avail_w = screen_w - 250
    avail_h = screen_h

    scale_x = max(1, avail_w // _config.WIDTH)
    scale_y = max(1, avail_h // _config.HEIGHT)
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
            color = _config.COLORS[xvar.color_palette].get(val, 0xFFFFFFFF)
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

    if hasattr(_config, 'DELAY') and _config.DELAY > 0:
        time.sleep(_config.DELAY)


def update_cell(xvar: XVar, mx: int, my: int, val: int,
                _config: config.Config) -> None:
    """
    Update a single cell in the maze rendering.

    Args:
        xvar (XVar): The graphics context.
        mx (int): The x-coordinate of the cell.
        my (int): The y-coordinate of the cell.
        val (int): The new value of the cell.
        _config (config.Config): The configuration instance.
    """
    if not xvar or not xvar.img_data:
        return

    try:
        screen_w = xvar.screen_w if xvar.screen_w else 1920
        screen_h = xvar.screen_h if xvar.screen_h else 1080
    except Exception:
        screen_w = 1920
        screen_h = 1080

    avail_w = screen_w - 250
    avail_h = screen_h

    scale_x = max(1, avail_w // _config.WIDTH)
    scale_y = max(1, avail_h // _config.HEIGHT)
    scale = min(scale_x, scale_y, 16)

    color_int = _config.COLORS[xvar.color_palette].get(val, 0xFFFFFFFF)
    color_bytes = color_int.to_bytes(4, 'little')

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
