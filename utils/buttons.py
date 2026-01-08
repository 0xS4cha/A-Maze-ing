#!/usr/bin/env python3

from utils.mlx_utils import XVar, manage_close
import exception
from utils.maze_utils import generate_maze, render_maze_to_mlx
from config import Config

mouse_callbacks = {}


def mouse_handler(btn_type, x, y, arg):
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


def draw_buttons(xvar: XVar):
    mlx = xvar.mlx
    mlx_ptr = xvar.mlx_ptr

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

        # Fake bold for better visibility (scaling not supported by MLX)
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
               callback,
               args):
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


def button_exit(xvar: XVar):
    manage_close(xvar)


def button_restart(config: Config, xvar: XVar):
    maze = generate_maze(config, xvar)
    render_maze_to_mlx(xvar.mlx, xvar.mlx_ptr, xvar.win_1, maze, config, xvar)


def buttons_init(config: Config, xvar: XVar):
    win_w = xvar.win_w if xvar.win_w else 800
    win_h = xvar.win_h if xvar.win_h else 600

    btn_bg_exit = 0xFFFFB7B2    # Pastel Red/Pink
    btn_bg_reload = 0xFFB5EAD7  # Pastel Mint Green
    btn_bg_path = 0xFFC7CEEA    # Pastel Periwinkle Blue
    btn_bg_color = 0xFFE2F0CB   # Pastel Lime/Yellow
    
    text_color = 0xFF555555  

    btn_width = 180
    btn_height = 45
    spacing = 15

    ui_panel_width = 250
    panel_start_x = win_w - ui_panel_width
    center_x = panel_start_x + (ui_panel_width - btn_width) // 2
    total_height = (btn_height * 4) + (spacing * 3)
    start_y = (win_h - total_height) // 2

    if start_y < 20:
        start_y = 20
    current_y = start_y

    def create_btn(name, text, bg_color, callback, args={}):
        add_button(name, center_x, current_y, btn_width, btn_height, 
                   text, bg_color, text_color, callback, args)

    create_btn("button_restart", "NEW MAZE", btn_bg_reload, button_restart, {"config": config, "xvar": xvar})
    current_y += btn_height + spacing
    
    create_btn("button_path", "SHOW PATH", btn_bg_path, button_restart, {"config": config, "xvar": xvar})
    current_y += btn_height + spacing
    
    create_btn("button_color", "ROTATE COLORS", btn_bg_color, button_restart, {"config": config, "xvar": xvar})
    current_y += btn_height + spacing
    
    create_btn("button_exit", "EXIT", btn_bg_exit, button_exit, {"xvar": xvar})

    xvar.mlx.mlx_mouse_hook(xvar.win_1, mouse_handler, None)
    draw_buttons(xvar)
