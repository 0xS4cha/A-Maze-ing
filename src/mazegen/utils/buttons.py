#!/usr/bin/env python3

from ..utils.mlx_utils import XVar, manage_close, update_cell
from .. import exception
from ..utils.maze_utils import generate_maze, render_maze_to_mlx
from ..config import Config
from typing import Callable, Any


mouse_callbacks: dict[str, Any] = {}
ui_bg_img = None


def mouse_handler(btn_type: int, x: int, y: int, arg: None) -> None:
    try:
        if btn_type != 1:
            return

        for name, data in mouse_callbacks.items():
            bx, by = data["x"], data["y"]
            bw, bh = data["w"], data["h"]

            if bx <= x < bx + bw and by <= y < by + bh:
                data["callback"](**data.get("args", {}))
    except SystemExit:
        raise SystemExit(0)


def draw_buttons(xvar: XVar) -> None:
    global ui_bg_img
    mlx = xvar.mlx
    mlx_ptr = xvar.mlx_ptr

    ui_width = 250
    win_w = xvar.win_w if xvar.win_w else 800
    win_h = xvar.win_h if xvar.win_h else 600
    panel_x = win_w - ui_width

    if ui_bg_img is None:
        ui_bg_img = mlx.mlx_new_image(mlx_ptr, ui_width, win_h)
        if ui_bg_img:
            bg_color_int = 0xFF323232

            buf, bpp, sl, fmt = mlx.mlx_get_data_addr(ui_bg_img)
            color_bytes = bg_color_int.to_bytes(4, "little")

            for y in range(win_h):
                off = y * sl
                for x in range(ui_width):
                    i = off + x * 4
                    if i + 4 <= len(buf):
                        buf[i:i+4] = color_bytes

    if ui_bg_img:
        mlx.mlx_put_image_to_window(mlx_ptr, xvar.win_1, ui_bg_img, panel_x, 0)

    for data in mouse_callbacks.values():
        bx, by = data["x"], data["y"]
        bw, bh = data["w"], data["h"]

        if data["img"] is None:
            img = mlx.mlx_new_image(mlx_ptr, bw, bh)
            if not img:
                raise exception.ConfigException("Cannot create MLX image")

            data["img"] = img

            buf, bpp, sl, fmt = mlx.mlx_get_data_addr(img)
            color = data["bg"].to_bytes(4, "little")

            for y in range(bh):
                off = y * sl
                for x in range(bw):
                    i = off + x * 4
                    buf[i:i+4] = color

        mlx.mlx_put_image_to_window(mlx_ptr, xvar.win_1, data["img"], bx, by)

        text = data["text"]
        tx = bx + (bw - len(text) * 10) // 2
        ty = by + (bh - 20) // 2

        mlx.mlx_string_put(mlx_ptr, xvar.win_1, tx, ty, data["fg"], text)


def add_button(name: str,
               x: int, y: int,
               w: int, h: int,
               text: str,
               bg: int,
               fg: int,
               callback: Callable,
               args: dict[str, Any]) -> None:
    mouse_callbacks[name] = {
        "x": x,
        "y": y,
        "w": w,
        "h": h,
        "bg": bg,
        "fg": fg,
        "text": text,
        "img": None,
        "callback": callback,
        "args": args
    }


def button_exit(xvar: XVar) -> None:
    manage_close(xvar)


def button_restart(config: Config, xvar: XVar) -> None:
    xvar.maze_data = generate_maze(config, xvar)
    render_maze_to_mlx(xvar.mlx, xvar.mlx_ptr, xvar.win_1, xvar.maze_data,
                       config, xvar)


def button_color_maze(config: Config, xvar: XVar) -> None:
    color_max = len(config.COLORS)
    xvar.color_palette = (xvar.color_palette + 1) % color_max
    render_maze_to_mlx(xvar.mlx, xvar.mlx_ptr, xvar.win_1, xvar.maze_data,
                       config, xvar)
    if xvar.show_path:
        button_toggle_path(config, xvar, xvar.show_path)


def button_toggle_path(config, xvar: XVar,
                       status: bool | None = None) -> None:
    colors = {True: 5, False: 0}
    if status is not None:
        xvar.show_path = status
    else:
        xvar.show_path = not xvar.show_path
    for x, y in xvar.path:
        update_cell(xvar, x, y, colors[xvar.show_path], config)


def buttons_init(config: Config, xvar: XVar) -> None:
    win_w = xvar.win_w if xvar.win_w else 800
    win_h = xvar.win_h if xvar.win_h else 600

    btn_bg_exit = 0xFFFFB7B2    # Pastel Red/Pink
    btn_bg_reload = 0xFFB5EAD7  # Pastel Mint Green
    btn_bg_path = 0xFFC7CEEA    # Pastel Periwinkle Blue
    btn_bg_color = 0xFFE2F0CB   # Pastel Lime/Yellow

    text_color = 0xFF555555

    btn_width = 180

    base_btn_h = 45
    base_spacing = 15
    num_btns = 4

    required_h = (base_btn_h * num_btns) + (base_spacing * (num_btns - 1)) + 40

    if win_h < required_h:
        avail_h = max(win_h - 40, 40)
        btn_height = int(avail_h / 5)
        spacing = int(btn_height / 3)
        if btn_height < 20:
            btn_height = 20
            spacing = 5
    else:
        btn_height = base_btn_h
        spacing = base_spacing

    ui_panel_width = 250
    panel_start_x = win_w - ui_panel_width
    center_x = panel_start_x + (ui_panel_width - btn_width) // 2
    total_height = (btn_height * 4) + (spacing * 3)
    start_y = (win_h - total_height) // 2

    if start_y < 20:
        start_y = 20
    current_y = start_y

    global mouse_callbacks
    mouse_callbacks = {}

    global ui_bg_img
    if ui_bg_img:
        xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, ui_bg_img)
        ui_bg_img = None

    def create_btn(name: str, text: str, bg_color: int, callback: Callable,
                   args: dict[str, Any] = {}) -> None:
        add_button(name, center_x, current_y, btn_width, btn_height,
                   text, bg_color, text_color, callback, args)

    create_btn("button_restart", "NEW MAZE", btn_bg_reload, button_restart,
               {"config": config, "xvar": xvar})
    current_y += btn_height + spacing

    create_btn("button_path", "SHOW PATH", btn_bg_path, button_toggle_path,
               {"config": config, "xvar": xvar})
    current_y += btn_height + spacing

    create_btn("button_color_maze", "ROTATE COLORS", btn_bg_color,
               button_color_maze, {"config": config, "xvar": xvar})
    current_y += btn_height + spacing

    create_btn("button_exit", "EXIT", btn_bg_exit, button_exit, {"xvar": xvar})

    xvar.mlx.mlx_mouse_hook(xvar.win_1, mouse_handler, None)
    draw_buttons(xvar)
