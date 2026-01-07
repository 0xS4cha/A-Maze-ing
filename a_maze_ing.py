#!/usr/bin/env python3

import sys
import exception
import config
from mlx import Mlx
from utils.mlx_utils import manage_expose, manage_close, manage_key_simple
from utils.mlx_utils import XVar, render_maze_to_mlx
from utils.maze_utils import generate_maze


def regenerate_maze_wrapper(xvar):
    if xvar.config and xvar.maze is not None:
        maze = generate_maze(xvar.config, xvar)
        xvar.maze = maze
        if xvar.show_path:
             entry = tuple(xvar.config.ENTRY)
             exit_p = tuple(xvar.config.EXIT)
             xvar.path = solve_bfs(maze, entry, exit_p)
        else:
             xvar.path = []

        render_maze_to_mlx(xvar.mlx, xvar.mlx_ptr, xvar.win_1, maze,
                           xvar.config, xvar)


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
            
            xvar.win_1 = xvar.mlx.mlx_new_window(xvar.mlx_ptr, win_w, win_h,
                                                 "A-Maze-ing")
            if not xvar.win_1:
                raise Exception("Can't create MLX window")
            
            xvar.regenerate_callback = lambda: regenerate_maze_wrapper(xvar)

            xvar.mlx.mlx_key_hook(xvar.win_1, manage_key_simple, xvar)
            xvar.mlx.mlx_hook(xvar.win_1, 33, 0, manage_close, xvar)
            xvar.mlx.mlx_expose_hook(xvar.win_1, manage_expose, xvar)

            maze = generate_maze(_config, xvar)
            render_maze_to_mlx(xvar.mlx, xvar.mlx_ptr, xvar.win_1, maze,
                               _config, xvar)
        except Exception as e:
            raise exception.ConfigException(f"MLX error: {e}")

        xvar.mlx.mlx_loop(xvar.mlx_ptr)
        print("destroy win(s)")
        xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win_1)
        print("destroy mlx")
        xvar.mlx.mlx_release(xvar.mlx_ptr)


if __name__ == "__main__":
    try:
        main()
    except (exception.ArgsException, exception.ConfigException) as e:
        exception.display_errors(e)
    except Exception as e:
        exception.display_errors(f"An unexpected error occurred: {e}")
