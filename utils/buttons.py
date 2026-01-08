#!/usr/bin/env python3

from utils.mlx_utils import XVar
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


def button_exit():
    exit(0)


def button_restart(config: Config, xvar: XVar):
    maze = generate_maze(config, xvar)
    render_maze_to_mlx(xvar.mlx, xvar.mlx_ptr, xvar.win_1, maze, config, xvar)


def buttons_init(config: Config, xvar: XVar):
    win_w = xvar.win_w if xvar.win_w else 800
    add_button("button_exit", win_w - 220, 20, 200, 50, "Exit", 0xffffffff, 0xff0000ff, button_exit, {})
    add_button("button_restart", win_w - 220, 80, 200, 50, "Reload", 0xffffffff, 0xff0000ff, button_restart,
               {"config": config, "xvar": xvar})

    xvar.mlx.mlx_mouse_hook(xvar.win_1, mouse_handler, None)
    draw_buttons(xvar)
