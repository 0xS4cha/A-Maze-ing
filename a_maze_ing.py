#!/usr/bin/env python3

import sys
import exception
import config
from mlx import Mlx
from utils.mlx_utils import manage_expose, manage_close, manage_key_simple
from utils.mlx_utils import XVar, render_maze_to_mlx, calculate_window_size
from utils.maze_utils import generate_maze
from utils.buttons import mouse_handler, buttons_init, draw_buttons


def main_expose(xvar):
    manage_expose(xvar)
    draw_buttons(xvar)


def main():
    xvar = XVar()
    try:
        xvar.mlx = Mlx()
    except Exception as e:
        raise exception.ConfigException(f"Can't initialize MLX: {e}")

    if len(sys.argv) <= 1:
        raise exception.ArgsException("Not enough arguments")
    try:
        _config = config.Config(sys.argv[1])
    except Exception as e:
        raise exception.ConfigException(f"Bad config file: {e}")
    if _config.WIDTH < 30 or _config.HEIGHT < 20:
        raise exception.ConfigException("Window size too small, minimum (w30, h20)")
    if _config.WIDTH % 2 == 0 or _config.HEIGHT % 2 == 0:
        raise exception.ConfigException("The window size cannot be even")
    if _config.GRAPHIC:
        try:
            xvar.mlx_ptr = xvar.mlx.mlx_init()
            ret, xvar.screen_w, xvar.screen_h = xvar.mlx.mlx_get_screen_size(
                xvar.mlx_ptr)

            required_w, required_h, _ = calculate_window_size(
                _config,
                xvar.screen_w,
                xvar.screen_h,
                ui_width=250
            )

            xvar.win_w = required_w
            xvar.win_h = required_h
            xvar.win_1 = xvar.mlx.mlx_new_window(xvar.mlx_ptr, required_w,
                                                 required_h,
                                                 "A-Maze-ing")
            if not xvar.win_1:
                raise Exception("Can't create MLX window")

            xvar.mlx.mlx_mouse_hook(xvar.win_1, mouse_handler, xvar)
            xvar.mlx.mlx_key_hook(xvar.win_1, manage_key_simple, xvar)
            xvar.mlx.mlx_hook(xvar.win_1, 33, 0, manage_close, xvar)
            xvar.mlx.mlx_expose_hook(xvar.win_1, main_expose, xvar)

            maze = generate_maze(_config, xvar)
            render_maze_to_mlx(xvar.mlx, xvar.mlx_ptr, xvar.win_1, maze,
                               _config, xvar)
        except Exception as e:
            raise exception.ConfigException(f"MLX error: {e}")

        buttons_init(_config, xvar)
        draw_buttons(xvar)

        xvar.mlx.mlx_loop(xvar.mlx_ptr)
        xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win_1)
        xvar.mlx.mlx_release(xvar.mlx_ptr)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except (exception.ArgsException, exception.ConfigException) as e:
        exception.display_errors(e)
    except Exception as e:
        exception.display_errors(f"An unexpected error occurred: {e}")
