#!/usr/bin/env python3

import sys
import exception
import config
from mlx import Mlx
from utils.mlx_utils import manage_expose, manage_close, manage_key_simple
from utils.mlx_utils import XVar, render_maze_to_mlx
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

    if _config.GRAPHIC:
        try:
            xvar.mlx_ptr = xvar.mlx.mlx_init()
            ret, xvar.screen_w, xvar.screen_h = xvar.mlx.mlx_get_screen_size(
                xvar.mlx_ptr)

            # Adjust window width logic to accommodate UI
            # We want to use as much space as possible but valid
            avail_w = xvar.screen_w if xvar.screen_w else 1920
            avail_h = xvar.screen_h if xvar.screen_h else 1080

            win_w = min(1920, avail_w)
            win_h = min(1080, avail_h)

            xvar.win_w = win_w
            xvar.win_h = win_h
            xvar.win_1 = xvar.mlx.mlx_new_window(xvar.mlx_ptr, win_w, win_h,
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
