#!/usr/bin/env python3

import random
from . import exception
from . import config
import secrets
from mlx import Mlx
from .utils.mlx_utils import manage_expose, manage_close, manage_key_simple
from .utils.mlx_utils import XVar, render_maze_to_mlx, calculate_window_size
from .utils.maze_utils import generate_maze as utils_generate_maze
from .utils.buttons import mouse_handler, buttons_init, draw_buttons


class MazeGenerator:
    def __init__(self, path: str):
        self.__xvar = XVar()
        try:
            self.__xvar.mlx = Mlx()
        except Exception as e:
            raise exception.ConfigException(f"Can't initialize MLX: {e}")

        self.__config = config.Config(path)
        if self.__config.WIDTH < 30 or self.__config.HEIGHT < 20:
            raise exception.ConfigException("Window size too small, \
minimum 30x20")
        if self.__config.WIDTH % 2 == 0 or self.__config.HEIGHT % 2 == 0:
            raise exception.ConfigException("The window size cannot be even")
        try:
            if self.__config.SEED == 0:
                seed = secrets.token_hex(8)
                random.seed(seed)
                print(seed)
            else:
                random.seed(self.__config.SEED)
            self.__xvar.mlx_ptr = self.__xvar.mlx.mlx_init()
            ret, self.__xvar.screen_w, self.__xvar.screen_h =\
                self.__xvar.mlx.mlx_get_screen_size(self.__xvar.mlx_ptr)

            required_w, required_h, _ = calculate_window_size(
                self.__config,
                self.__xvar.screen_w,
                self.__xvar.screen_h,
                ui_width=250
            )

            self.__xvar.win_w = required_w
            self.__xvar.win_h = required_h
            self.__xvar.win_1 = self.__xvar.mlx.mlx_new_window(
                self.__xvar.mlx_ptr, required_w,
                required_h,
                "A-Maze-ing"
            )
            if not self.__xvar.win_1:
                raise Exception("Can't create MLX window")

            self.__xvar.mlx.mlx_mouse_hook(
                self.__xvar.win_1,
                mouse_handler,
                self.__xvar
            )
            self.__xvar.mlx.mlx_key_hook(
                self.__xvar.win_1,
                manage_key_simple,
                self.__xvar
            )
            self.__xvar.mlx.mlx_hook(
                self.__xvar.win_1,
                33, 0,
                manage_close,
                self.__xvar
            )
            self.__xvar.mlx.mlx_expose_hook(
                self.__xvar.win_1,
                self.__main_expose,
                self.__xvar
            )
        except Exception as e:
            raise exception.ConfigException(f"MLX error: {e}")

        buttons_init(self.__config, self.__xvar)
        draw_buttons(self.__xvar)

    def __main_expose(self, xvar):
        manage_expose(xvar)
        draw_buttons(xvar)

    def generate_maze(self):
        self.__xvar.maze_data = utils_generate_maze(self.__config, self.__xvar)
        return self.__xvar.maze_data

    def draw_maze(self, maze):
        render_maze_to_mlx(
            self.__xvar.mlx,
            self.__xvar.mlx_ptr,
            self.__xvar.win_1,
            maze,
            self.__config,
            self.__xvar
        )

    def draw_control_buttons(self):
        buttons_init(self.__config, self.__xvar)
        draw_buttons(self.__xvar)

    def run(self):
        self.__xvar.mlx.mlx_loop(self.__xvar.mlx_ptr)
        self.__xvar.mlx.mlx_destroy_window(
            self.__xvar.mlx_ptr,
            self.__xvar.win_1
        )
        self.__xvar.mlx.mlx_release(self.__xvar.mlx_ptr)
