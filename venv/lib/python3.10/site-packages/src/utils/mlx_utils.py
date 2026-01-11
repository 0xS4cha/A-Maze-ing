"""MLX utility functions for the maze generator."""
from .. import config
from .. import exception
from mlx import Mlx
import time
from typing import Any, List, Union
from ..utils.generate_utils import Bit_position


class XVar:
    """Class to hold X window server variables and MLX state."""

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
        self.path_img = None
        self.img_data = None
        self.img_bpp = 0
        self.img_sl = 0
        self.img_format = 0
        self.img_w = 0
        self.img_h = 0


def manage_close(xvar: XVar) -> None:
    """
    Handle window close event.

    Args:
        xvar (XVar): The graphics context.
    """
    xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)


def manage_key_simple(key: int, xvar: XVar) -> None:
    """
    Handle key press events for closing the window with 'q' or ESC.

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
        tuple[int, int, int]: A tuple containing (required_width, \
required_height, cell_size).
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
    target_img = xvar.path_img if (
        xvar.show_path and xvar.path_img) else xvar.img
    if target_img:
        xvar.mlx.mlx_put_image_to_window(
            xvar.mlx_ptr,
            xvar.win_1,
            target_img,
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
    if xvar.path_img:
        mlx.mlx_destroy_image(mlx_ptr, xvar.path_img)
        xvar.path_img = None

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
    border_thick = max(1, scale // 5)

    img_w = _config.WIDTH * scale
    img_h = _config.HEIGHT * scale

    if xvar.img:
        mlx.mlx_destroy_image(mlx_ptr, xvar.img)

    img = mlx.mlx_new_image(mlx_ptr, img_w, img_h)
    if not img:
        raise exception.ConfigException("Can't create MLX image for maze \
rendering")

    data, bpp, sl, fmt = mlx.mlx_get_data_addr(img)

    wall_bytes = _config.COLORS[xvar.color_palette].get(
        1, 0x000000).to_bytes(4, 'little')
    path_bytes = _config.COLORS[xvar.color_palette].get(
        0, 0xFFFFFF).to_bytes(4, 'little')
    isolated_bytes = _config.COLORS[xvar.color_palette].get(
        2, 0xFF0000).to_bytes(4, 'little')
    start_bytes = _config.COLORS[xvar.color_palette].get(
        3, 0x00FF00).to_bytes(4, 'little')
    end_bytes = _config.COLORS[xvar.color_palette].get(
        4, 0x0000FF).to_bytes(4, 'little')

    for my in range(_config.HEIGHT):
        for mx in range(_config.WIDTH):
            cell = maze[my][mx]
            is_isolated = (cell & 15) == 0

            if mx == _config.ENTRY[0] and my == _config.ENTRY[1]:
                bg_bytes = start_bytes
            elif mx == _config.EXIT[0] and my == _config.EXIT[1]:
                bg_bytes = end_bytes
            elif is_isolated:
                bg_bytes = isolated_bytes
            else:
                bg_bytes = path_bytes

            start_y = my * scale
            start_x = mx * scale
            for dy in range(scale):
                py = start_y + dy
                row_off = py * sl
                for dx in range(scale):
                    px = start_x + dx
                    off = row_off + px * 4
                    if off + 4 <= len(data):
                        is_wall = False
                        if dy < border_thick and not (
                                cell & Bit_position.NORTH.value):
                            is_wall = True
                        elif dx >= scale - border_thick and not (
                                cell & Bit_position.EAST.value):
                            is_wall = True
                        elif dy >= scale - border_thick and not (
                                cell & Bit_position.SOUTH.value):
                            is_wall = True
                        elif dx < border_thick and not (
                                cell & Bit_position.WEST.value):
                            is_wall = True
                        if is_wall:
                            data[off:off+4] = wall_bytes
                        else:
                            data[off:off+4] = bg_bytes

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


def create_path_image(xvar: XVar, _config: config.Config) -> None:
    """Create a secondary image that includes the solution path."""
    if not xvar.img or not xvar.path:
        return

    scale = xvar.img_w // _config.WIDTH
    border_thick = max(1, scale // 5)
    sl = xvar.img_sl
    xvar.path_img = xvar.mlx.mlx_new_image(
        xvar.mlx_ptr, xvar.img_w, xvar.img_h)
    src_data = xvar.img_data
    dst_data, _, _, _ = xvar.mlx.mlx_get_data_addr(xvar.path_img)

    dst_data[:] = src_data[:]
    path_color = _config.COLORS[xvar.color_palette].get(
        5, 0x00FF00).to_bytes(4, 'little')
    for px, py in xvar.path:
        start_y = py * scale
        start_x = px * scale
        cell_mask = xvar.maze_data[py][px]
        for dy in range(scale):
            row_off = (start_y + dy) * sl
            for dx in range(scale):
                if (dy < border_thick and
                        not (cell_mask & Bit_position.NORTH.value)):
                    continue

                if (dx >= scale - border_thick and
                        not (cell_mask & Bit_position.EAST.value)):
                    continue

                if (dy >= scale - border_thick and
                        not (cell_mask & Bit_position.SOUTH.value)):
                    continue

                if (dx < border_thick and
                        not (cell_mask & Bit_position.WEST.value)):
                    continue
                off = row_off + (start_x + dx) * 4
                if off + 4 <= len(dst_data):
                    dst_data[off:off+4] = path_color


def update_cell(xvar: XVar, mx: int, my: int, val: Union[int, List[int]],
                _config: config.Config) -> None:
    """
    Update a single cell in the maze rendering.

    Args:
        xvar (XVar): The graphics context.
        mx (int): The x-coordinate of the cell.
        my (int): The y-coordinate of the cell.
        val (Union[int, List[int]]): The new value (int mask).
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
    border_thick = max(1, scale // 5)

    data = xvar.img_data
    sl = xvar.img_sl
    start_y = my * scale
    start_x = mx * scale

    wall_bytes = _config.COLORS[xvar.color_palette].get(
        1, 0x000000).to_bytes(4, 'little')
    path_bytes = _config.COLORS[xvar.color_palette].get(
        0, 0xFFFFFF).to_bytes(4, 'little')
    isolated_bytes = _config.COLORS[xvar.color_palette].get(
        2, 0xFF0000).to_bytes(4, 'little')
    start_bytes = _config.COLORS[xvar.color_palette].get(
        3, 0x00FF00).to_bytes(4, 'little')
    end_bytes = _config.COLORS[xvar.color_palette].get(
        4, 0x0000FF).to_bytes(4, 'little')

    mask = val if isinstance(val, int) else 0
    is_isolated = (mask & 15) == 0

    if mx == _config.ENTRY[0] and my == _config.ENTRY[1]:
        bg_bytes = start_bytes
    elif mx == _config.EXIT[0] and my == _config.EXIT[1]:
        bg_bytes = end_bytes
    elif is_isolated:
        bg_bytes = isolated_bytes
    else:
        bg_bytes = path_bytes
    for dy in range(scale):
        py = start_y + dy
        row_off = py * sl
        for dx in range(scale):
            px = start_x + dx
            off = row_off + px * 4
            if off + 4 <= len(data):
                is_wall = False
                if dy < border_thick and not (mask & Bit_position.NORTH.value):
                    is_wall = True
                elif (dx >= scale - border_thick and
                        not (mask & Bit_position.EAST.value)):
                    is_wall = True
                elif (dy >= scale - border_thick and
                        not (mask & Bit_position.SOUTH.value)):
                    is_wall = True
                elif dx < border_thick and not \
                        (mask & Bit_position.WEST.value):
                    is_wall = True

                if is_wall:
                    data[off:off+4] = wall_bytes
                else:
                    data[off:off+4] = bg_bytes

    xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, xvar.win_1, xvar.img, 0, 0)


__all__ = ["Bit_position"]
