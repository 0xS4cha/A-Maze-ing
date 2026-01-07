#!/usr/bin/env python3

import sys
import exception
import config
from mlx import Mlx
from utils.mlx_utils import manage_close, manage_key_simple, XVar
from utils.maze_utils import generate_maze


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

    generate_maze(_config)

    #try:
    #    xvar.mlx_ptr = xvar.mlx.mlx_init()
    #    ret, xvar.screen_w, xvar.screen_h = xvar.mlx.mlx_get_screen_size(
    #        xvar.mlx_ptr)
    #    win_w = min(400, xvar.screen_w if xvar.screen_w else 400)
    #    win_h = min(400, xvar.screen_h if xvar.screen_h else 400)
    #    xvar.win_1 = xvar.mlx.mlx_new_window(xvar.mlx_ptr, win_w, win_h,
    #                                         "A-Maze-ing")
    #    if not xvar.win_1:
    #        raise Exception("Can't create MLX window")
    #    xvar.mlx.mlx_key_hook(xvar.win_1, manage_key_simple, xvar)
    #    xvar.mlx.mlx_hook(xvar.win_1, 33, 0, manage_close, xvar)
    #except Exception as e:
    #    raise exception.ConfigException(f"MLX error: {e}")

    #xvar.mlx.mlx_loop(xvar.mlx_ptr)
    #print("destroy win(s)")
    #xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win_1)
    #print("destroy mlx")
    #xvar.mlx.mlx_release(xvar.mlx_ptr)


if __name__ == "__main__":
    try:
        main()
    except (exception.ArgsException, exception.ConfigException) as e:
        exception.display_errors(e)
    except Exception as e:
        exception.display_errors(f"An unexpected error occurred: {e}")
